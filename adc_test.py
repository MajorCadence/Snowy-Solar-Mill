from time import sleep
import mcp3008
voltages = []
adc = mcp3008.MCP3008(0, 0)
while True:
    try:
        voltages = adc.read_all(5)
        print(voltages[8:])
        sleep(0.5)
    except KeyboardInterrupt:
        break
adc.close()
