import matplotlib.pyplot as plt
import os

def read_data_from_file(filename):
    x_coords = []
    y_coords = []
    
    with open(filename, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file if line.strip() and not line.strip().startswith('#')]
        
        if not lines:
            return x_coords, y_coords
            
        first_line_parts = lines[0].split()
        
        if len(first_line_parts) == 1 and first_line_parts[0].isdigit():
            n_points = int(first_line_parts[0])
            data_lines = lines[1:n_points+1]
        else:
            data_lines = lines
            
        for line in data_lines:
            parts = line.split()
            if len(parts) >= 2:
                x_coords.append(float(parts[0]))
                y_coords.append(float(parts[1]))
                
    return x_coords, y_coords

def visualize_data(filename, x_coords, y_coords):
    fig, ax = plt.subplots(figsize=(12, 10))
    
    ax.plot(
        x_coords, 
        y_coords, 
        marker='o', 
        linestyle='None', 
        color='blue', 
        alpha=0.7, 
        label='Точки данных'
    )
    
    ax.set_aspect('equal', adjustable='box')
    
    ax.set_title(f'Визуализация данных: {os.path.basename(filename)}', fontsize=12, fontweight='bold')
    ax.set_xlabel('Координата X', fontsize=10)
    ax.set_ylabel('Координата Y', fontsize=10)
    
    ax.grid(axis='y', alpha=0.3)
    
    ax.legend(fontsize=10)

    if x_coords and y_coords:
        x_margin = (max(x_coords) - min(x_coords)) * 0.1 if max(x_coords) != min(x_coords) else 1.0
        y_margin = (max(y_coords) - min(y_coords)) * 0.1 if max(y_coords) != min(y_coords) else 1.0
        ax.set_xlim(min(x_coords) - x_margin, max(x_coords) + x_margin)
        ax.set_ylim(min(y_coords) - y_margin, max(y_coords) + y_margin)
    
    plt.tight_layout()
    
    output_filename = os.path.splitext(filename)[0] + '.png'
    plt.savefig(output_filename, dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    print(f'график {output_filename} сохранен')

def main():
    filenames = ['001.dat', '002.dat', '003.dat', '004.dat', '005.dat']
    
    for filename in filenames:
        if not os.path.exists(filename):
            print(f'файл {filename} не найден. Пропуск.')
            continue
        try:
            x_coords, y_coords = read_data_from_file(filename)
            print(f'файл {filename}: прочитано {len(x_coords)} точек')
            visualize_data(filename, x_coords, y_coords)
            
        except ValueError as e:
            print(f'ошибка формата данных в файле {filename}: {e}')
        except Exception as e:
            print(f'непредвиденная ошибка при обработке {filename}: {e}')


if __name__ == '__main__':
    main()