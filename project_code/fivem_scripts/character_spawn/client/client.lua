local spawnPos = vector3( -288.0, -508.0, 25.0)

AddEventHandler('onClientGameTypeStart', function()
    exports.spawnmanager:setAutoSpawnCallback(function()
        exports.spawnmanager:spawnPlayer({
            x = spawnPos.x,
            y = spawnPos.y,
            z = spawnPos.z,
            model = 'a_f_y_beach_01'
        }, function()
            TriggerEvent('chat:addMessage', {
                args = { 'Welcome to the party!!!' }
            })
        end)
    end)
    exports.spawnmanager:setAutoSpawn(true)
    exports.spawnmanager:forceRespawn()
end)


