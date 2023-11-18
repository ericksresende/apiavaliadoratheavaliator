import json
import os
import shutil
import traceback
import sys
sys.path.append("../")

from evaluator_code.command.evaluate_code import main_flow
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()

origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

async def process_submission(data):
    try:
        id = data['id']
        alunos = data['alunos']
        professor_code = data['professor']
        problema = data['problema']

        alunos_ids = [aluno['id'] for aluno in alunos]
        alunos_codes = [aluno['codigo'] for aluno in alunos]

        folder_path = f"{id}"
        print(folder_path)
        os.makedirs(os.path.join(folder_path, "alunos"), exist_ok=True)
        os.makedirs(os.path.join(folder_path, "professor"), exist_ok=True)

        for aluno in alunos:
            aluno_id = aluno['id']
            aluno_code = aluno['codigo']
            aluno_filename = f"{aluno_id}.py"
            aluno_filepath = os.path.join(folder_path, "alunos", aluno_filename)
            with open(aluno_filepath, 'w') as aluno_file:
                aluno_file.write(aluno_code)

        with open(os.path.join(folder_path, "professor", "professor.py"), 'w') as professor_file:
            professor_file.write(professor_code)

        current_directory = os.getcwd()
        # current_directory = "."
        full_folder_path = os.path.join(current_directory, folder_path)
        main_flow(folder_path, full_folder_path)

        with open(os.path.join(full_folder_path, folder_path), 'r') as json_file:
            dados = json.load(json_file)

        shutil.rmtree(folder_path)

        return dados

    except Exception as e:
        error_message = str(e)
        traceback_info = traceback.format_exc()
        shutil.rmtree(folder_path)

        response = {
            "error": error_message,
            "traceback": traceback_info
        }
        raise HTTPException(status_code=500, detail=response)

@app.post('/avaliarsubmissoes')
async def process_data(data: dict):
    results = await asyncio.gather(process_submission(data))
    return results[0]


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
