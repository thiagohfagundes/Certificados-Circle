# 1. Usamos a imagem do Python 3.11 como base
FROM python:3.11

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Copia os arquivos do seu projeto para o container
COPY . /app

# 4. Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# 5. Expõe a porta que a FastAPI vai usar (padrão: 8000)
EXPOSE 8000

# 6. Comando para iniciar a aplicação com uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]