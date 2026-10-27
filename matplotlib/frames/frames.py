import matplotlib.pyplot as plt
import os
import math


def read_frames(filename):
    frames = []
    
    with open(filename, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file if line.strip() and not line.strip().startswith('#')]

    for i in range(0, len(lines) - 1, 2):
        x_coords = [float(v) for v in lines[i].split()]
        y_coords = [float(v) for v in lines[i + 1].split()]
        frames.append((x_coords, y_coords))
    
    return frames


def get_global_bounds(frames):
    all_x = []
    all_y = []
    for x_coords, y_coords in frames:
        all_x.extend(x_coords)
        all_y.extend(y_coords)
    
    x_min, x_max = min(all_x), max(all_x)
    y_min, y_max = min(all_y), max(all_y)
    
    x_margin = (x_max - x_min) * 0.05 if x_max != x_min else 1.0
    y_margin = (y_max - y_min) * 0.05 if y_max != y_min else 1.0
    
    return (x_min - x_margin, x_max + x_margin, y_min - y_margin, y_max + y_margin)


def visualize_frames_grid(filename, frames):
    n_frames = len(frames)
    if n_frames == 0:
        print('нет кадров для отрисовки.')
        return
    
    n_cols = 2
    n_rows = math.ceil(n_frames / n_cols)
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 6 * n_rows))
    
    if n_rows == 1:
        axes = [axes]
    if n_rows == 1 and n_cols == 1:
        axes = [[axes]]
    
    x_min, x_max, y_min, y_max = get_global_bounds(frames)
    
    frame_idx = 0
    for row in range(n_rows):
        for col in range(n_cols):
            ax = axes[row][col]
            if frame_idx < n_frames:
                x_coords, y_coords = frames[frame_idx]
                ax.plot(x_coords, y_coords, color='blue', linewidth=1.5)
                ax.set_title(f'Frame {frame_idx}', fontsize=12, fontweight='bold')
                ax.set_xlim(x_min, x_max)
                ax.set_ylim(y_min, y_max)
                ax.grid(True, alpha=0.3)
                frame_idx += 1
            else:
                # Пустой subplot — скрываем
                ax.axis('off')
    
    plt.tight_layout()
    
    output_filename = os.path.splitext(filename)[0] + '_grid.png'
    plt.savefig(output_filename, dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    print(f'общий график {output_filename} сохранён ({n_frames} кадров)')


def visualize_frames_individual(filename, frames):
    n_frames = len(frames)
    if n_frames == 0:
        return
    
    x_min, x_max, y_min, y_max = get_global_bounds(frames)
    
    for idx, (x_coords, y_coords) in enumerate(frames):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x_coords, y_coords, color='blue', linewidth=1.5)
        ax.set_title(f'Frame {idx}', fontsize=12, fontweight='bold')
        ax.set_xlabel('X', fontsize=10)
        ax.set_ylabel('Y', fontsize=10)
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        output_filename = f'{os.path.splitext(filename)[0]}_frame_{idx:03d}.png'
        plt.savefig(output_filename, dpi=150, bbox_inches='tight')
        plt.close(fig)
    
    print(f'сохранено {n_frames} отдельных кадров для {filename}')


def main():
    filename = 'frames.dat'
    
    if not os.path.exists(filename):
        print(f'файл {filename} не найден.')
        return
    
    try:
        frames = read_frames(filename)
        print(f'файл {filename}: прочитано {len(frames)} кадров')
        
        visualize_frames_grid(filename, frames)
        
        visualize_frames_individual(filename, frames)
        
    except ValueError as e:
        print(f'ошибка формата данных: {e}')
    except Exception as e:
        print(f'непредвиденная ошибка: {e}')


if __name__ == '__main__':
    main()