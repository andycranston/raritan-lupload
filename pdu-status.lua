--
-- pdu-status.lua: show high level status information about a PDU
--

require "Pdu"

-- -------------------------------------------------------------

function powerstate2text(powerstate)
  if powerstate == pdumodel.Outlet.PowerState.PS_ON then
    text = "On"
  elseif powerstate == pdumodel.Outlet.PowerState.PS_OFF then
    text = "Off"
  else
    text = "*Unknown*"
  end

  return text
end

-- --------------------------------------------------------------

--
-- Main
--

local pdu = pdumodel.Pdu:getDefault()

local np = pdu:getNameplate()
local md = pdu:getMetaData()

io.write("***********************\n")
io.write("***********************\n")
io.write("* General Information *\n")
io.write("***********************\n")
io.write("***********************\n")
io.write("\n")

io.write("Model: " .. np.model .. "\n")
io.write("Serial number: " .. np.serialNumber .. "\n")
io.write("Firmware revison: " .. md.fwRevision .. "\n")
io.write("Hardware revison: " .. md.hwRevision .. "\n")
io.write("\n")

io.write("**********************\n")
io.write("* Outlet Information *\n")
io.write("**********************\n")
io.write("\n")

local outlets = pdu:getOutlets()

for i,outlet in ipairs(outlets) do
  local outletname = outlet:getSettings().name
  local outletstate = outlet:getState()
  local powerstate = outletstate.powerState
  local cycleflag = outletstate.cycleInProgress
  
  if outletname == "" then
    outletname = "*no name*"
  end
  io.write("Outlet# " .. tostring(i) .. "\n")
  io.write("  Name: " .. outletname .. "\n")
  io.write("  Power state: " .. powerstate2text(powerstate))
  if cycleflag then
    io.write(" (power cycle in progress)")
  end
  io.write("\n")
  -- printTable(outletstate)
end

io.write("\n")

io.write("****************\n")
io.write("* End of report*\n")
io.write("****************\n")

os.exit(0)
