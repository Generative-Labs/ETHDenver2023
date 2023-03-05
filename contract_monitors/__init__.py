from contract_monitors.Aragon import ARAGON_CONTRACT_ADDR, ARAGON_Parser
from contract_monitors.USDC import USDC_CONTRACT_ADDR, USDC_Parser
from contract_monitors.USDT import USDT_CONTRACT_ADDR, USDT_Parser
from contract_monitors.tBTC import tBTC_CONTRACT_ADDR, tBTC_Parser


CONTRACT_PARSERS = {
    tBTC_CONTRACT_ADDR: tBTC_Parser,
    ARAGON_CONTRACT_ADDR: ARAGON_Parser,
    USDC_CONTRACT_ADDR: USDC_Parser,
    USDT_CONTRACT_ADDR: USDT_Parser,
}
