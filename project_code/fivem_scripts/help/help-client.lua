RegisterCommand("help", function()
    msg("1st line message!")
    msg("2nd line message!")
end, false)

function msg(text)
    TriggerEvent("chatMessage", "[terminal]", {255,0,0}, text)
end 