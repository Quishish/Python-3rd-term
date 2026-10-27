import matplotlib.pyplot as plt
import os
from collections import defaultdict


def read_data(filename):
    records = []
    
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split(';')
            if len(parts) >= 3:
                prep = parts[0].strip()
                group = parts[1].strip()
                try:
                    mark = int(parts[2].strip())
                    records.append((prep, group, mark))
                except ValueError:
                    continue
    
    return records


def compute_stats(records, key_index):
    counts = defaultdict(lambda: defaultdict(int))
    all_marks = set()
    all_keys = set()
    
    for prep, group, mark in records:
        key = (prep, group)[key_index]
        counts[key][mark] += 1
        all_marks.add(mark)
        all_keys.add(key)
    
    keys = sorted(all_keys)
    marks = sorted(all_marks)
    
    return keys, marks, counts


def plot_stacked_bar(keys, marks, counts, title, xlabel, output_filename):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors = {
        3:  '#cc0000',
        4:  '#e68a00',
        5:  '#ffcc00',
        6:  '#aacc00',
        7:  '#66b300',
        8:  '#339900',
        9:  '#008000',
        10: '#006600',
    }
    
    bottom = {key: 0 for key in keys}
    
    for mark in marks:
        heights = [counts[key].get(mark, 0) for key in keys]
        color = colors.get(mark, '#aaaaaa')
        ax.bar(keys, heights, bottom=[bottom[key] for key in keys],
               color=color, label=str(mark), edgecolor='white', linewidth=0.5)
        for i, key in enumerate(keys):
            bottom[key] += heights[i]
    
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel('количество студентов', fontsize=10)
    ax.legend(title='оценка', fontsize=9, title_fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_filename, dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    print(f'график {output_filename} сохранён')


def analyze_records(records):
    prep_stats = defaultdict(list)
    group_stats = defaultdict(list)
    
    for prep, group, mark in records:
        prep_stats[prep].append(mark)
        group_stats[group].append(mark)
    
    def avg_and_fail(marks_list):
        avg = sum(marks_list) / len(marks_list)
        fail_ratio = sum(1 for m in marks_list if m <= 3) / len(marks_list)
        return avg, fail_ratio
    
    print('\nанализ препов')
    prep_avgs = {p: avg_and_fail(ms) for p, ms in prep_stats.items()}
    sorted_by_avg = sorted(prep_avgs.items(), key=lambda x: x[1][0], reverse=True)
    
    print('cамые халявные (высокий средний балл):')
    for prep, (avg, fail) in sorted_by_avg[:3]:
        print(f'  {prep}: средний балл {avg:.2f}, доля троек и ниже {fail:.1%}')
    
    print('факеры (низкий средний балл):')
    for prep, (avg, fail) in sorted_by_avg[-3:]:
        print(f'  {prep}: средний балл {avg:.2f}, доля троек и ниже {fail:.1%}')
    
    print('\nанализ групп')
    group_avgs = {g: avg_and_fail(ms) for g, ms in group_stats.items()}
    sorted_by_fail = sorted(group_avgs.items(), key=lambda x: x[1][1], reverse=True)
    
    print('самая раздолбайская группа (наибольшая доля троек и ниже):')
    for group, (avg, fail) in sorted_by_fail[:3]:
        print(f'  {group}: средний балл {avg:.2f}, доля троек и ниже {fail:.1%}')


def main():
    filename = 'students.csv'
    
    if not os.path.exists(filename):
        print(f'файл {filename} не найден.')
        return
    
    try:
        records = read_data(filename)
        print(f'файл {filename}: прочитано {len(records)} записей')
        
        prep_keys, marks, prep_counts = compute_stats(records, key_index=0)
        plot_stacked_bar(
            prep_keys, marks, prep_counts,
            title='Marks per prep',
            xlabel='Препод',
            output_filename='marks_per_prep.png'
        )
        
        group_keys, marks, group_counts = compute_stats(records, key_index=1)
        plot_stacked_bar(
            group_keys, marks, group_counts,
            title='Marks per group',
            xlabel='Группа',
            output_filename='marks_per_group.png'
        )

        analyze_records(records)
        
    except Exception as e:
        print(f'непредвиденная ошибка: {e}')


if __name__ == '__main__':
    main()