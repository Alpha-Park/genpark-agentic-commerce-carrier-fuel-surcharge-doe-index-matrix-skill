# Freight Carrier DOE Weekly Diesel Fuel Surcharge (FSC) Matrix Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `calculate_freight_fsc_surcharge`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Calculates contractually enforceable Freight Fuel Surcharges (FSC) linked to US Energy Information Administration (EIA/DOE) On-Highway Diesel weekly indexes.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Agentic Commerce (Logistics & Freight Auditing)`

## MCP Tool Specification
### `calculate_freight_fsc_surcharge`
Parameters:
- `current_doe_diesel_price_per_gallon` (float): Current DOE National On-Highway Diesel average ($/gal)
- `base_peg_price_per_gallon` (float): Contract base fuel peg (e.g. $1.25 or $2.50)
- `fsc_increment_interval_cents` (float): Price change interval per tier (e.g. $0.05 or $0.06)
- `fsc_surcharge_per_interval_cents` (float): Additional surcharge per interval (e.g. $0.01/mile or 0.5%)
- `total_linehaul_miles` (float): Total billable linehaul distance (miles)
- `billed_carrier_fsc_amount_usd` (float): Fuel surcharge amount billed by carrier on invoice

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-agentic-commerce-carrier-fuel-surcharge-doe-index-matrix-skill": {
      "command": "python",
      "args": ["/path/to/genpark-agentic-commerce-carrier-fuel-surcharge-doe-index-matrix-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
