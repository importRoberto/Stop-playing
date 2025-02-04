import time
import psutil
import os
import platform

# Tempo principal + tempo de encerramento, em segundos
TEMPO_PROCESSO = 35 * 60
TEMPO_EXTRA = 20

# Tempo em que o som fica ligado, em milissegundos
TEMPO_EXTRA_SOM = 3 * 1000

# Nome do processo (verifique no Gerenciador de Tarefas)
PROCESSO = "SkyrimSE.exe"


# Verifica se um processo está rodando e retorna sua referência (PID)
def encontrar_processo(nome):
    for processo in psutil.process_iter(attrs=["pid", "name"]):
        if processo.info["name"] == nome:
            return processo.info["pid"]
    return None


#Encerra um processo pelo PID.
def encerrar_processo(pid):
    try:
        os.kill(pid, 9)  # 9 força o encerramento
        print(f"Processo {PROCESSO} encerrado!")
    except Exception as e:
        print(f"Erro ao encerrar o processo: {e}")

#Reproduz um aviso sonoro.
def tocar_som():
    sistema = platform.system()
    
    if sistema == "Windows":
        import winsound
        winsound.Beep(110, TEMPO_EXTRA_SOM)
            
    #Se você está em outra plataforma
    elif sistema == "Linux":
        os.system("aplay /usr/share/sounds/alsa/Front_Center.wav")  # Som padrão do Linux
    elif sistema == "Darwin":  # macOS
        os.system("afplay /System/Library/Sounds/Glass.aiff")  # Som padrão do macOS
    else:
        print("\a")  # Beep genérico (pode não funcionar em alguns sistemas)

def main():
    print("Timer iniciado! Você tem %d minutos para jogar." % (TEMPO_PROCESSO/60))
    time.sleep(TEMPO_PROCESSO)

    # Aviso para o usuário
    print("\nTempo acabou! Você tem %d segundos para salvar e sair!" % (TEMPO_EXTRA))
    tocar_som()  # Toca o som de alerta
    time.sleep(TEMPO_EXTRA)

    # Verifica e encerra o jogo se ainda estiver rodando
    pid = encontrar_processo(PROCESSO)
    if pid:
        encerrar_processo(pid)
    else:
        print("O jogo já foi fechado.")

if __name__ == "__main__":
    main()
