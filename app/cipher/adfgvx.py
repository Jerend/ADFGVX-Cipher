import random
import math

ADFGVX_LETTERS = ['A', 'D', 'F', 'G', 'V', 'X']

class ADFGVXCipher:
    def __init__(self):
        self.grid = None
        self.keyword = None
    
    def generate_grid(self, custom_alphabet: str = None):
        """Генерирует случайную таблицу шифра 6x6"""
        if custom_alphabet:
            alphabet = custom_alphabet
        else:
            alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        
        shuffled = list(alphabet)
        random.shuffle(shuffled)
        
        self.grid = {}
        for i, row_char in enumerate(ADFGVX_LETTERS):
            for j, col_char in enumerate(ADFGVX_LETTERS):
                idx = i * 6 + j
                if idx < len(shuffled):
                    self.grid[shuffled[idx]] = (row_char, col_char)
        
        return self.grid
    
    def load_grid(self, grid_data):
        """Загружает таблицу шифра из словаря"""
        self.grid = grid_data
        return self.grid
    
    def generate_permutation_table(self, keyword: str):
        """Генерирует таблицу перестановки на основе ключевого слова"""
        self.keyword = keyword.upper()
        sorted_keyword = ''.join(sorted(self.keyword))
        
        permutation = []
        for char in self.keyword:
            positions = [i for i, c in enumerate(sorted_keyword) if c == char]
            if positions:
                pos = positions.pop(0)
                sorted_keyword = sorted_keyword[:pos] + '_' + sorted_keyword[pos+1:]
                permutation.append(pos)
        
        permutation_table = []
        for col_index in sorted(range(len(self.keyword)), key=lambda x: permutation.index(x) if x in permutation else x):
            col_letter = self.keyword[permutation.index(col_index)] if col_index in permutation else None
            if col_letter:
                permutation_table.append({
                    'original_index': col_index,
                    'new_index': permutation.index(col_index),
                    'letter': col_letter
                })
        
        return {
            'keyword': self.keyword,
            'permutation_order': permutation,
            'table': permutation_table
        }
    
    def encrypt(self, plaintext: str) -> str:
        """Шифрование текста"""
        if not self.grid:
            raise ValueError("Таблица шифра не сгенерирована")
        if not self.keyword:
            raise ValueError("Ключевое слово для перестановки не задано")
        
        plaintext = ''.join([c.upper() for c in plaintext if c.isalnum()])
        
        # Замена символов на пары ADFGVX
        encoded = []
        for char in plaintext:
            if char in self.grid:
                encoded.append(self.grid[char][0] + self.grid[char][1])
        
        encoded_str = ''.join(encoded)
        
        # Перестановка
        cols = len(self.keyword)
        rows = math.ceil(len(encoded_str) / cols)
        
        matrix = []
        for i in range(rows):
            row = []
            for j in range(cols):
                idx = i * cols + j
                if idx < len(encoded_str):
                    row.append(encoded_str[idx])
                else:
                    row.append('')
            matrix.append(row)
        
        perm_table = self.generate_permutation_table(self.keyword)
        perm_order = perm_table['permutation_order']
        
        result = []
        for col_idx in perm_order:
            for row in matrix:
                if row[col_idx]:
                    result.append(row[col_idx])
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str) -> str:
        """Дешифрование текста"""
        if not self.grid:
            raise ValueError("Таблица шифра не загружена")
        if not self.keyword:
            raise ValueError("Ключевое слово для перестановки не задано")
        
        reverse_grid = {v: k for k, v in self.grid.items()}
        
        cols = len(self.keyword)
        total_len = len(ciphertext)
        rows = math.ceil(total_len / cols)
        last_row_len = total_len % cols
        if last_row_len == 0:
            last_row_len = cols
        
        perm_table = self.generate_permutation_table(self.keyword)
        perm_order = perm_table['permutation_order']
        
        col_lengths = [rows] * cols
        for i in range(cols):
            if i >= last_row_len:
                col_lengths[i] -= 1
        
        matrix = [['' for _ in range(cols)] for _ in range(rows)]
        
        idx = 0
        for col_idx in perm_order:
            for row in range(col_lengths[col_idx]):
                if idx < total_len:
                    matrix[row][col_idx] = ciphertext[idx]
                    idx += 1
        
        encoded = []
        for row in range(rows):
            for col in range(cols):
                if matrix[row][col]:
                    encoded.append(matrix[row][col])
        
        encoded_str = ''.join(encoded)
        
        result = []
        for i in range(0, len(encoded_str), 2):
            if i + 1 < len(encoded_str):
                pair = encoded_str[i] + encoded_str[i+1]
                for char, code in reverse_grid.items():
                    if code == pair:
                        result.append(char)
                        break
        
        return ''.join(result)