RegisterCommand('obj',function(source, args, raw)
    local playerPed = GetPlayerPed(-1) -- get the player's ped
    local coords = GetEntityCoords(playerPed) -- get the player's coordinates
    --local object = CreateObject(GetHashKey("prop_vodka_bottle"), coords.x, coords.y, coords.z, true, true, true) -- create the object at the player's coordinates
    local object = GetHashKey("weapon_pumpshotgun")
    local compoent = GetHashKey("COMPONENT_AT_SR_SUPP")
    -- AttachEntityToEntity(object, playerPed, GetPedBoneIndex(playerPed, 60309), 0.05, -0.2, 0.01, -90.0, 0.0, 0.0, true, true, false, true, 1, true) -- attach the object to the player's hand
    -- GiveWeaponObjectToPed(object, playerPed)
    GiveWeaponComponentToPed(playerPed, object, compoent)
end)

