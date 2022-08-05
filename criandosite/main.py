from comunidadeimpressionadora import app #como ta importando do arquivo __init__ só coloca o nome da pasta e oq vai importar
#se for importar algo de outro arquivo que não seja o __init__ 'comunidadeimpressionadora.models' exemplo.
if __name__ == '__main__':  ##isso só ira ser execultado se for o arquivo main
    app.run(debug=True)  # modo debug não precisa ficar pausando o código e executando novamente, cada alteração sera feita direta no site
