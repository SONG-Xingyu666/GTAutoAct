------------------------ Main Variables ------------------------ 
-- Mod start flag
local flag = false
-- Index of position
local pos_index = 1
-- Index of weather
local weather_index = 1
-- Index of ped 
local ped_index = 1
-- Index of the time of the day
local time_index = 1
-- Play ID
local playerId = PlayerId()


------------------------ Register Commmand ------------------------
-- Start "change_environment" mod if 'env' is called
RegisterCommand('env', function(source, args, raw)
    flag = true
end)
-- Set player to invincible
SetEntityInvincible(GetPlayerPed(), true)



------------------------ Loop ------------------------
-- Create thread for Waitting the instruction call
Citizen.CreateThread(function()
    while true do 
        Citizen.Wait(1)
        -- Change_environment starts
        if (flag == true) then
            -- Goto next location
            if (IsDisabledControlPressed(1, Cfg.controls.keyboard.nextLoc)) then
                toNextLocation()
                Citizen.Wait(100)
            end
            -- Goto a random location
            if (IsDisabledControlPressed(1, Cfg.controls.keyboard.ranLoc)) then
                toRandomLoaction()
                Citizen.Wait(100)
            end
            -- Change the weather
            if (IsDisabledControlPressed(1, Cfg.controls.keyboard.changeWeather)) then
                changeWeather()
                Citizen.Wait(100)
            end
            -- Change the ped
            if (IsDisabledControlPressed(1, Cfg.controls.keyboard.changePed)) then
                changePed()
                Citizen.Wait(100)
            end
            -- Change the time
            if (IsDisabledControlPressed(1, Cfg.controls.keyboard.changeTime)) then
                changeTime()
                Citizen.Wait(100)
            end     
        end
    end
end)


------------------------ Functions ------------------------
function changeWeather()
    weather_index = weather_index + 1
    SetWeatherTypeNowPersist(Cfg.weather[weather_index])
    if weather_index > #Cfg.weather then
        weather_index = 1
    end
    print('change weather '..Cfg.weather[weather_index])   
end

function toNextLocation()
    pos_index = pos_index + 1
    if pos_index > #Cfg.locations then
        pos_index = 1
    end
    SetEntityCoords(PlayerPedId(), tonumber(Cfg.locations[pos_index][1]), tonumber(Cfg.locations[pos_index][2]), tonumber(Cfg.locations[pos_index][3]))
    print('go to next position '..pos_index)
end

function toRandomLoaction()
    local ranLocIndex = math.random(1, #Cfg.locations)
    SetEntityCoords(PlayerPedId(), tonumber(Cfg.locations[ranLocIndex][1]), tonumber(Cfg.locations[ranLocIndex][2]), tonumber(Cfg.locations[ranLocIndex][3]))
end

function changePed()
    ped_index = ped_index + 1
    if ped_index > #Cfg.peds then
        ped_index = 1
    end
    -- Get the player's Ped ID
    local pedID = GetHashKey(Cfg.peds[ped_index])
    -- Request the model to make sure it's available
    RequestModel(pedID)
    -- Wait for the model to load
    while not HasModelLoaded(pedID) do
    Citizen.Wait(0)
    end
    -- Set the player's model to the new Ped ID
    SetPlayerModel(PlayerId(), pedID)
    -- Set the player's default spawn info so that they don't spawn in the wrong place
    SetPedDefaultComponentVariation(PlayerPedId())
    -- Mark the model as no longer needed to free up memory
    SetModelAsNoLongerNeeded(pedID)
    print('change ped')
end

function changeTime()
    time_index = time_index + 1
    if time_index > #Cfg.time then
        time_index = 1
    end
    NetworkOverrideClockTime(hour, min, sec)
    hour = Cfg.time[time_index][1]
    min = Cfg.time[time_index][2]
    sec =  Cfg.time[time_index][3]
end