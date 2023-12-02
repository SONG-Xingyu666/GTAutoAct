
RegisterNetEvent('animation:write_duration', function(dict, animation, duration)

    TriggerEvent('chat:addMessage', playerId, {
        args = {' duration ' ..duration}
    })
    file = io.open('animation_lists\\text.txt', 'a')
    file:write(dict)
    file:write(' ')
    file:write(animation)
    file:write(' ')
    file:write(duration)
    file:write('\n')
    file:close()
end)