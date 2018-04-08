start "game1" python game\game_server.py 8885 8881 8882 8883

start "game2" python game\game_server.py 8886 8882 8881 8883

start "game3" python game\game_server.py 8887 8883 8881 8882

timeout 3

start "gate" python gate\gate_server.py 8880 8885 8886 8887