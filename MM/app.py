import streamlit as st
import time
import numpy as np

def print_matrix(matrix):
    """Retorna uma string com a matriz formatada com 2 casas decimais."""
    return "\n".join("\t".join(f"{x:.2f}" for x in row) for row in matrix)

def swap_rows(matrix, row1, row2):
    """Troca duas linhas da matriz."""
    matrix[[row1, row2]] = matrix[[row2, row1]]

def eliminate_column(matrix, pivot_row, pivot_col):
    """Zera os elementos abaixo do pivô na coluna especificada."""
    for row in range(pivot_row + 1, len(matrix)):
        if matrix[row, pivot_col] != 0:
            factor = matrix[row, pivot_col] / matrix[pivot_row, pivot_col]
            matrix[row] -= factor * matrix[pivot_row]

def escalona_matriz(matrix):
    """
    Converte a matriz para sua forma escalonada por meio da eliminação de Gauss.
    Retorna uma lista com as etapas e a matriz escalonada final.
    """
    rows, cols = matrix.shape
    pivot_row = 0
    steps = []
    
    for col in range(cols - 1):
        if pivot_row >= rows:
            break
        
        max_row = pivot_row + np.argmax(np.abs(matrix[pivot_row:, col]))
        if matrix[max_row, col] == 0:
            continue
        
        if max_row != pivot_row:
            swap_rows(matrix, pivot_row, max_row)
        
        eliminate_column(matrix, pivot_row, col)
        steps.append(np.copy(matrix))
        pivot_row += 1
    
    return steps, matrix

def canonica_matriz(matrix):
    """
    Converte a matriz escalonada para sua forma canônica, eliminando os coeficientes acima dos pivôs.
    """
    rows, cols = matrix.shape
    for row in range(rows - 1, -1, -1):
        nonzero = np.where(np.abs(matrix[row, :-1]) > 1e-8)[0]
        if nonzero.size == 0:
            continue
        leading_col = nonzero[0]
        matrix[row] /= matrix[row, leading_col]
        for upper_row in range(row):
            factor = matrix[upper_row, leading_col]
            matrix[upper_row] -= factor * matrix[row]
    return matrix

def verificar_solucao(matrix):
    """
    Determina se o sistema possui solução única ou infinitas soluções.
    Retorna:
      - status: 'solucao_unica' ou 'infinitas'
      - solução (apenas se única)
      - colunas com pivôs
      - conjunto de variáveis livres
    """
    rows, cols = matrix.shape
    num_vars = cols - 1
    pivot_columns = []
    
    for row in range(rows):
        nonzero = np.where(np.abs(matrix[row, :-1]) > 1e-8)[0]
        if nonzero.size > 0:
            pivot_columns.append(nonzero[0])
    
    free_variables = set(range(num_vars)) - set(pivot_columns)
    
    if len(pivot_columns) == num_vars:
        solution = np.zeros(num_vars)
        for i, col in enumerate(pivot_columns):
            solution[col] = matrix[i, -1]
        return 'solucao_unica', solution, pivot_columns, free_variables
    else:
        return 'infinitas', None, pivot_columns, free_variables

def expressao_solucao(matrix, pivot_columns, free_variables):
    """
    Expressa a solução geral do sistema em termos das variáveis livres.
    Cada variável livre é representada por um parâmetro t com o índice da variável.
    """
    rows, cols = matrix.shape
    num_vars = cols - 1
    sol_expressao = [None] * num_vars
    
    # Expressa as variáveis básicas em função das variáveis livres
    for i, col in enumerate(pivot_columns):
        expr = f"{matrix[i, -1]:.2f}"
        for j in free_variables:
            coef = -matrix[i, j]
            if abs(coef) > 1e-8:
                expr += f" {'+' if coef > 0 else '-'} {abs(coef):.2f}t{j}"
        sol_expressao[col] = expr
    
    # Para as variáveis livres, a solução é o parâmetro t correspondente
    for var in free_variables:
        sol_expressao[var] = f"t{var}"
    
    return sol_expressao

def main():
    st.title("Calculadora de Sistemas de Equações Lineares")
    st.subheader("Por :blue[André Jordan] e :blue[Reyso Teixeira] :sunglasses:")
    st.write("Forneça os dados do sistema linear.")
    
    # Entrada do usuário: número de equações e variáveis
    m = st.number_input("Número de equações:", min_value=1, step=1, value=3)
    n = st.number_input("Número de variáveis:", min_value=1, step=1, value=3)
    
    st.write("Insira a matriz aumentada. Cada linha corresponde a uma equação e deve conter os coeficientes seguidos do termo independente, separados por espaço ou vírgula.")
    st.write(f"Exemplo para {m} equações e {n} variáveis (cada linha deve conter {n+1} valores):")
    
    exemplo = "\n".join([" ".join(["0", "1", "3", "-2"]) for _ in range(m)])
    user_input = st.text_area("Matriz aumentada:", exemplo)
    
    if st.button("Processar"):
        progress_text = "Pedindo ajuda dos universitários..."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()
        
        try:
            # Processa a entrada e cria a matriz (m x (n+1))
            lines = user_input.strip().split("\n")
            if len(lines) != m:
                st.error(f"Esperado {m} linhas, mas foram fornecidas {len(lines)}.")
                return
            
            data = []
            for line in lines:
                parts = [float(x) for x in line.replace(',', ' ').split()]
                if len(parts) != (n+1):
                    st.error(f"Cada linha deve ter {n+1} valores. Verifique a linha: {line}")
                    return
                data.append(parts)
            matrix = np.array(data, dtype=float)
            
            st.subheader("Matriz inicial:")
            st.text(print_matrix(matrix))
            
            # Realiza a eliminação gaussiana (forma escalonada)
            steps, escalonada = escalona_matriz(np.copy(matrix))
            for i, step in enumerate(steps):
                st.subheader(f"Após etapa {i+1}:")
                st.text(print_matrix(step))
            
            st.subheader("Matriz escalonada obtida:")
            st.text(print_matrix(escalonada))
            
            # Converte para forma canônica
            canonica = canonica_matriz(np.copy(escalonada))
            st.subheader("Forma canônica obtida:")
            st.text(print_matrix(canonica))
            
            # Verifica a solução e exibe os resultados
            status, sol, pivot_columns, free_variables = verificar_solucao(canonica)
            if status == 'solucao_unica':
                st.subheader("O sistema possui solução única:")
                st.write(sol)
            else:
                st.subheader("O sistema possui infinitas soluções.")
                st.write(f"Quantidade de variáveis livres: {len(free_variables)}")
                sol_expressao = expressao_solucao(canonica, pivot_columns, free_variables)
                st.subheader("Solução geral:")
                for i, expr in enumerate(sol_expressao):
                    st.write(f"x{i} = {expr}")
                    
        except Exception as e:
            st.error(f"Erro ao processar a entrada: {e}")

if __name__ == '__main__':
    main()
