while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #창닫기
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:  #키보드가 눌림
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:  #아래방향키 or s키
                selected = (selected + 1) % len(menu_items)
            elif event.key == pygame.K_UP or event.key == pygame.K_w:  #위방향키 or w키
                selected = (selected - 1) % len(menu_items)
            elif event.key == pygame.K_RETURN:
                run_selected(selected)
