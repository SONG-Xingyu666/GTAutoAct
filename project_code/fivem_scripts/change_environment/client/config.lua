------------------------ Configurations for change_environment ------------------------ 
Cfg = {}
Cfg.useCommand = true
Cfg.command = "env"

Cfg.controls = {
    keyboard = {
        nextLoc = 197, -- ]
        ranLoc = 116, -- [
        changeWeather = 56, -- F9
        changePed = 57, -- F10
        changeTime = 344, -- F11
        -- nextPos = 107, -- NUMPAD 6
        -- lastPos = 108, -- NUMPAD 4
        -- changeWeather = 117, -- NUMPAD 7
        -- changePed = 118, -- NUMPAD 9
        -- changeTime = 314, -- NUMPAD +
    }
}

Cfg.peds = {
    -- "a_m_m_bevhills_02",
    -- "a_m_m_eastsa_02",
    -- "a_m_m_soucent_02",
    -- "a_m_y_beachvesp_02",
    -- "s_m_m_gaffer_01",
    -- "a_m_m_farmer_01",
    -- "mp_m_securoguard_01",
    -- "s_m_m_scientist_01",
    -- "a_m_m_tennis_01",
    -- "a_f_y_tennis_01",
    -- "a_f_y_runner_01",
    -- "a_m_y_breakdance_01",
    -- "a_f_m_ktown_01",

    -- "u_f_y_corpse_02",
    -- "csb_denise_friend",
    -- "a_f_y_fitness_02",

    
    "a_f_m_bevhills_02",
    "ig_abigail",
    "s_f_y_ranger_01",
    "s_f_y_cop_01",

    "a_f_y_beach_01",
    "u_m_m_jesus_01",
    -- "a_f_m_bodybuild_01",
    -- "a_m_y_beach_03",
    -- "a_m_y_musclbeac_01",
    -- "a_m_y_surfer_01",
    -- "s_f_y_baywatch_01",

    -- Terrorists
    -- "s_m_y_prisoner_01",
    -- "s_m_y_swat_01",
    -- "u_m_m_edtoh",
    -- "u_m_y_tattoo_01",

    -- 'a_f_m_beach_01',
    -- 'a_f_y_beach_01',
    -- 'a_f_y_fitness_02',
    -- 'a_m_m_beach_02',
    -- 'a_m_y_breakdance_01',
    -- 'a_m_y_musclbeac_01',
    -- 'cs_maryann',
    -- 'csb_denise_friend',

    -- 'a_m_m_bevhills_01', 
    -- 'g_f_y_vagos_01',
    -- 'g_m_importexport_01',
    -- 'mp_f_cocaine_01',

    -- 's_m_m_movalien_01',
    -- 's_m_m_movspace_01',


}


Cfg.locations = {
    {1405.0, 1500.0, 113.0}, -- open Field
    -- {998.0, 2379.0, 52.0}, -- constructionSite
    -- {-346.0, 6494.0, 3.0}, -- beach
    -- {2641.0, 4610.0, 37.0}, -- farmLand  
    {-1177.0, -1665.0, 4.0}, -- tennisCourt 
    -- {-1248.0, -1090.0, 8.0}, -- neighborhood  
    -- {-248.0, -314.0, 30.0}, -- shoppingMall  
    -- {-662.0, 254.0, 81.0}, -- downtown  
    {-1117.0, 26.0, 51.0}, -- golfCourse  
    -- {129.0, -631.0, 263.0}, -- skyscraperRoof  
    -- {637.0, -1522.0, 10.0}, -- underBridge 
    -- {-408.0, -2282.0, 8.0}, -- port 
    -- {-486.0, 7708.0, 0.0}, -- sea 

    {-2361.0, 3245.0, 93.0}, -- office  
    -- {618.0, 2761.0, 42.0}, -- clothesStore  
    -- {-2141.0, 3255.0, 33.0}, -- aircraftWarehouse  
    -- {-3.0, 523.0, 175.0}, -- indoorHouse  
    -- {-167.0, -298.0, 40.0}, -- fittingRoom 
    -- {-298.0, -324.0, 10.0}, -- subwayStatioin  
    -- {413.0, -1325.0, 41.0}, -- parkingBuilding 
    -- {2737.0, 1663.0, -22.0}, -- Garage  

    -- smash windows
    -- {140.0, -745.0, 258.0},
    -- {140.0, -746.0, 242.0},

    -- NTU
    -- {-288.0, -508.0, 25.0},
    -- {-1746.0, 171.0, 64.0},
    -- {220.0, -3259.0, 41.0},
}

Cfg.outLocations = {
    {1405.0, 1500.0, 113.0}, -- open Field
    {998.0, 2379.0, 52.0}, -- constructionSite
    {-346.0, 6494.0, 3.0}, -- beach
    {2641.0, 4610.0, 37.0}, -- farmLand  
    {-1177.0, -1665.0, 4.0}, -- tennisCourt 
    {-1248.0, -1090.0, 8.0}, -- neighborhood  
    {-248.0, -314.0, 30.0}, -- shoppingMall  
    {-662.0, 254.0, 81.0}, -- downtown  
    {-1086.0, 8.0, 51.0}, -- golfCourse  
    {129.0, -631.0, 263.0}, -- skyscraperRoof  
    {637.0, -1522.0, 10.0}, -- underBridge 
    {-408.0, -2282.0, 8.0}, -- port 
}

Cfg.inLocations = {
    {-2361.0, 3245.0, 93.0}, -- office  
    {618.0, 2761.0, 42.0}, -- clothesStore  
    {-2141.0, 3255.0, 33.0}, -- aircraftWarehouse  
    {-3.0, 523.0, 175.0}, -- indoorHouse  
    {-167.0, -298.0, 40.0}, -- fittingRoom 
    {-298.0, -324.0, 10.0}, -- subwayStatioin  
    {413.0, -1325.0, 41.0}, -- parkingBuilding 
    {2737.0, 1663.0, -22.0}, -- Garage 
}

Cfg.weather = {
    'EXTRASUNNY',
    'CLEAR',
    'NEUTRAL',
    'SMOG',
    'FOGGY',
    'OVERCAST',
    'CLOUDS',
    'CLEARING',
    'RAIN',
    'THUNDER',
    'SNOW',
    'BLIZZARD',
    'SNOWLIGHT',
    'XMAS',
    'HALLOWEEN',
}

Cfg.time = {
    {8, 0, 0}, -- 5:30:00 sunrise 
    {9, 0, 0}, -- 12:00:00 noon 
    {10, 0, 0},
    {11, 0, 0},
    {12, 0, 0},
    {13, 0, 0},
    {14, 0, 0},
    {15, 0, 0},

    {20, 0, 0}, -- 20:00:00 sunset 
    {23, 0, 0}, -- 23:00:00 midnight
}