import pygame

def debug_sdl_events():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    
    # 启用所有可能的事件类型
    pygame.event.set_allowed(None)  # 先禁止所有
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.TEXTINPUT, pygame.TEXTEDITING])
    
    # 启用文本输入
    pygame.key.start_text_input()
    pygame.key.set_text_input_rect(pygame.Rect(100, 100, 600, 400))
    
    events_log = []
    running = True
    
    while running and len(events_log) < 20:  # 只记录前20个事件
        for event in pygame.event.get():
            event_info = f"Event: {event.type}"
            
            if event.type == pygame.QUIT:
                running = False
            elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                event_info += f" | KEY: {event.key} | Unicode: {event.unicode} | Name: {pygame.key.name(event.key)}"
            elif event.type == pygame.TEXTINPUT:
                event_info += f" | TEXT: {event.text}"
            elif event.type == pygame.TEXTEDITING:
                event_info += f" | EDIT: {event.text} @ {event.start}"
            
            events_log.append(event_info)
            print(event_info)  # 控制台输出
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        
        # 显示事件日志
        screen.fill((0, 0, 0))
        for i, log in enumerate(events_log[-15:]):  # 显示最后15个事件
            text_surface = font.render(log, True, (255, 255, 255))
            screen.blit(text_surface, (10, 10 + i * 25))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    return events_log

if __name__ == "__main__":
    events = debug_sdl_events()
    print("\n=== 事件记录 ===")
    for event in events:
        print(event)