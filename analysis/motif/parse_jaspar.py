def parse_jaspar(jaspar_file):
    """解析 JASPAR 格式的 PWM 文件"""
    motifs = {}
    current_id = None
    current_name = None
    current_rows = []  # 存 A/C/G/T 四行

    with open(jaspar_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_id is not None:
                    # 把 4 行转成 (4, L) 矩阵
                    matrix = []
                    for row in current_rows:
                        matrix.append(row)
                    motifs[current_id] = {
                        'name': current_name,
                        'matrix': matrix  # shape (4, L)
                    }
                parts = line[1:].split('\t')
                current_id = parts[0]
                current_name = parts[1] if len(parts) > 1 else parts[0]
                current_rows = []
            elif line and line[0] in 'ACGT':
                nums = line.split('[')[1].split(']')[0].split()
                current_rows.append([float(x) for x in nums])

    if current_id is not None:
        matrix = []
        for row in current_rows:
            matrix.append(row)
        motifs[current_id] = {
            'name': current_name,
            'matrix': matrix
        }

    return motifs

if __name__ == '__main__':
    motifs = parse_jaspar('JASPAR2024_CORE_plants_non-redundant_pfms_jaspar.txt')
    print(f'Total motifs: {len(motifs)}')
    for i, (mid, m) in enumerate(list(motifs.items())[:5]):
        print(f'{mid}: {m["name"]}, matrix shape=({len(m["matrix"])}, {len(m["matrix"][0])})')
