import matplotlib.pyplot as plt
import pandas as pd


def analyze_g_and_h_students(
    excel_path: str = "students_info.xlsx", ejudge_path: str = "results_ejudge.html"
):
  """Определяет, из каких факультетских групп пришли и в какие группы по информатике

  попали студенты, которые смогли пройти более одного теста (>10 баллов)
  в хотя бы одной из двух последних задач (G и H), и строит график.
  """
  # Загрузка данных из Excel с распределением групп
  students_df = pd.read_excel(excel_path)

  # Загрузка таблицы результатов из HTML
  ejudge_tables = pd.read_html(ejudge_path)
  ejudge_df = ejudge_tables[0]

  # Если заголовки многоуровневые, схлопываем их в одну строку
  if isinstance(ejudge_df.columns, pd.MultiIndex):
    ejudge_df.columns = [
        "_".join(str(c) for c in col if c) for col in ejudge_df.columns
    ]

  # Автоматический поиск колонки с логином/пользователем (в HTML-файле это 'User')
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

  # Ищем названия колонок, соответствующих задачам G и H
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

  # Переводим задачи G и H в числовой формат
  for task in target_tasks:
    ejudge_df[task] = pd.to_numeric(ejudge_df[task], errors="coerce").fillna(0)

  # Условие: пройдено более одного теста (> 10 баллов) в задачах G или H
  condition = False
  for task in target_tasks:
    condition = condition | (ejudge_df[task] > 10)

  successful_logins = ejudge_df[condition]["login"].unique()

  # Объединяем с информацией о группах
  full_merged = pd.merge(students_df, ejudge_df, on="login", how="inner")
  successful_students = full_merged[full_merged["login"].isin(successful_logins)]

  if successful_students.empty:
    print(
        "Внимание: Не найдено студентов, удовлетворяющих условию, либо не"
        " сошлись логины между файлами."
    )
    return None, None

  # Подсчет статистики для графиков
  faculty_sources = successful_students["group_faculty"].value_counts()
  out_groups = successful_students["group_out"].value_counts()

  # Построение графиков
  fig, axes = plt.subplots(1, 2, figsize=(14, 6))

  faculty_sources.plot(
      kind="bar",
      ax=axes[0],
      color="skyblue",
      legend=False,
  )
  axes[0].set_title(
      "Успешные студенты (задачи G/H) по факультетским группам", fontsize=11
  )
  axes[0].set_ylabel("Количество студентов")
  axes[0].tick_params(axis="x", rotation=45)

  out_groups.plot(
      kind="bar",
      ax=axes[1],
      color="lightgreen",
      legend=False,
  )
  axes[1].set_title(
      "Успешные студенты (задачи G/H) по группам по информатике", fontsize=11
  )
  axes[1].set_ylabel("Количество студентов")
  axes[1].tick_params(axis="x", rotation=45)

  plt.tight_layout()
  plt.savefig("successful_students_g_h.png")
  print("\nГрафик успешно сохранен в файл 'successful_students_g_h.png'.")
  plt.show()

  return faculty_sources, out_groups


if __name__ == "__main__":
  analyze_g_and_h_students("students_info.xlsx", "results_ejudge.html")