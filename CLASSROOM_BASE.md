# 오늘 수업 코드와의 연결

LEC16_Time의 main.py, game_framework.py, game_world.py를 원본 그대로 가져온 뒤 과제에 필요한 부분을 단계적으로 수정한다.

play_mode.py는 오늘 수업과 같은 init/handle_events/update/render/finish/pause/resume 구조다. 기존 Boy와 Grass 등록을 새 10마리 등록으로 교체하며, game_world.add_oject/update/render/clear 흐름을 유지한다. add_oject의 수업 코드 이름도 유지했다.

Bird.update()는 수업에서 배운 game_framework.frame_time으로 이동과 날갯짓을 갱신한다. animation.py는 그 계산을 검증할 수 있도록 분리한 시간 모델이다.

원본 SHA-256:
- main.py: `3ee958f13c17db9fb9a08f06ce1a1960c4195a167de99ede561b14dc01fd5847`
- game_framework.py: `f6fd71b0ff2635b7ca02c68610e0cdb029571bd7e2679194fb5d7b4c6ecfb578`
- game_world.py: `83d3a2f5f0e256a7ae0419a6a3570f52945b5285de218dba1e0715549f370557`
- play_mode.py: `34c8bae80db3199dc779d5f74e69df519c41f89d830140f88dfec0524743ca91`
- bird_animation.png: `9bc76685a79754b32235a3144c0f82ccbac2695cbeae76e4dcc1339a566c16b7`
