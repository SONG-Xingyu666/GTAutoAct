RegisterCommand('p', function()
    local dictName = 'export@sta006' -- .ycd file
    local animName = 'sta006' -- .onim file
  
    -- Request animation dictionary.
    RequestAnimDict(dictName)
    while not HasAnimDictLoaded(dictName) do
      Wait(1)
    end
  
    -- Play animation on player ped.
    local playerPed = PlayerPedId()
    TaskPlayAnim(playerPed, dictName, animName, 20.0, 8.0, 0.1, 0.1, 2.0)
    -- TaskPlayAnimAdvanced(playerPed, dictName, animName, -1219.0, -1583.0, 3.0)
  
    -- Unload animation dictionary.
    RemoveAnimDict(dictName)
  end, false)
