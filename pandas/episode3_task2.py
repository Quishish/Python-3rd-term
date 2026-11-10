import pandas as pd


def analyze_g_and_h_students(
    excel_path: str = "students_info.xlsx", ejudge_path: str = "results_ejudge.html"
):

  students_df = pd.read_excel(excel_path)

  ejudge_tables = pd.read_html(ejudge_path)
  ejudge_df = ejudge_tables[0]

  if isinstance(ejudge_df.columns, pd.MultiIndex):
    ejudge_df.columns = [
        "_".join(str(c) for c in col if c) for col in ejudge_df.columns
    ]

  login_col = None
  for col in ejudge_df.columns:
    col_lower = str(col).lower()
    if any(
        kw in col_lower
        for kw in ["user", "login", "логин", "участник", "id", "пользователь"]
    ):
      login_col = col
      break

  if login_col is None:
    login_col = ejudge_df.columns[1]

  ejudge_df = ejudge_df.rename(columns={login_col: "login"})

  if "login" not in students_df.columns:
    for col in students_df.columns:
      if str(col).lower() in ["login", "логин"]:
        students_df = students_df.rename(columns={col: "login"})
        break

  target_tasks = [
      col
      for col in ejudge_df.columns
      if str(col).strip().upper() in ["G", "H", "ЗАДАЧА G", "ЗАДАЧА H"]
  ]
  if not target_tasks:
    target_tasks = [
        col
        for col in ejudge_df.columns
        if "g" in str(col).lower() or "h" in str(col).lower()
    ]

  print(f"Используемые колонки для задач G/H: {target_tasks}")

  if not target_tasks:
    print(
        "Ошибка: Не удалось найти колонки для задач G и H в HTML-файле."
        " Проверьте их названия."
    )
    return None, None

  for task in target_tasks:
    ejudge_df[task] = pd.to_numeric(ejudge_df[task], errors="coerce").fillna(0)

  condition = False
  for task in target_tasks:
    condition = condition | (ejudge_df[task] > 10)

  successful_logins = ejudge_df[condition]["login"].unique()

  full_merged = pd.merge(students_df, ejudge_df, on="login", how="inner")
  successful_students = full_merged[full_merged["login"].isin(successful_logins)]

  if successful_students.empty:
    print(
        "Внимание: Не найдено студентов, удовлетворяющих условию, или логины"
        " не совпали."
    )
    return None, None

  faculty_sources = successful_students["group_faculty"].value_counts()
  out_groups = successful_students["group_out"].value_counts()

  print("\n--- Факультетские группы успешных студентов ---")
  print(faculty_sources)

  print("\n--- Целевые группы по информатике успешных студентов ---")
  print(out_groups)

  return faculty_sources, out_groups


if __name__ == "__main__":
  analyze_g_and_h_students("students_info.xlsx", "results_ejudge.html")