import alpha_beta_agent
import CameraVision
import socket


TCP_IP = '192.168.100.100'
TCP_PORT = 5000
BUFFER_SIZE = 1024

def send_decision(decision):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(str(decision).encode('utf-8'))
    data = s.recv(BUFFER_SIZE)
    print("Response from robot: ", data)
    s.close()


if __name__ == "__main__":
    print("Welcome to the Connet-4 AI client")
    decision = 4
    cvt = CameraVision.CameraVision()
    while decision > 0:
        input("Press any key when the human player is done with his turn...")
        print("Running camera")
        fl_grid = cvt.run()
        grid = []
        for row in fl_grid:
            grid.append([int(i) for i in row])
        print("Asking the AI what to do")
        decision = alpha_beta_agent.makeDecision(grid)
        print("Sending decision: Play on column ", decision)
        send_decision(decision)
    print("Game over")
    if decision == 0:
        print("No winner I guess")
    elif decision == -1:
        print("The robot won the game! What will it do next??")
    else:
        print("The human won, there is still hope")
    cvt.abort()
