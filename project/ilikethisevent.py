def handle_events():
    global player
    global bossList
    global bulletList
    global coinList
    global powerUpList
    global boomUpList
    global boomList
    global minion1List
    global minion2List
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        # command Locate
            # key down
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            if event.key == SDLK_0:
                coinList += [Coin((400,300))]
            if event.key == SDLK_1:
                powerUpList += [PowerUp((400,300))]
            if event.key == SDLK_2:
                boomUpList += [BoomUp((400,300))]

            if event.key == SDLK_RIGHT:
                player.setDirectX(1)
            elif event.key == SDLK_LEFT:
                player.setDirectX(-1)
            if event.key == SDLK_UP:
                player.setDirectY(1)
            elif event.key == SDLK_DOWN:
                player.setDirectY(-1)

            if event.key == SDLK_z:
                player.isCharge(True)
                # nomalBullet
                bulletList+=[kirbyBullet1(player.getPoint())]
            if event.key == SDLK_x:
                player.setBoom(-1)
                boomList+=[kirbyBoom(player.getPoint())]
                # useBoom

            if event.key == SDLK_b:
                bossList += [Boss()]
            if event.key == SDLK_m:
                minion1List += [Minion1(0)]
                minion1List += [Minion1(1)]
                minion1List += [Minion1(2)]
                minion1List += [Minion1(3)]
            if event.key == SDLK_n:
                minion2List += [Minion2()]
            if event.key == SDLK_v:
                for boss in bossList:
                    boss.Kill()

            # key down

            # key up
        if event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                player.setDirectX(-1)
            elif event.key == SDLK_LEFT:
                player.setDirectX(1)
            if event.key == SDLK_UP:
                player.setDirectY(-1)
            elif event.key == SDLK_DOWN:
                player.setDirectY(1)

            if event.key == SDLK_z:
                if player.getState() == kirbyStatus.READY:
                    if player.getCount() >= 35:
                        # charge Shot
                        bulletList+=[maxBullet(player.getPoint())]
                        player.setState(kirbyStatus.SHOT)
                    else:
                        # nomalBullet
                        bulletList+=[kirbyBullet2(player.getPoint())]
                        player.setState(kirbyStatus.IDLE)
                    player.setFrameYZero()
                player.resetCount()
                player.isCharge(False)
            # key up
        # command Locate