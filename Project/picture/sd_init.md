# Entity: sd_init 

- **File**: sd_init.vhd
## Diagram

![Diagram](sd_init.svg "Diagram")
## Generics

| Generic name  | Type              | Value                                         | Description                                   |
| ------------- | ----------------- | --------------------------------------------- | --------------------------------------------- |
| cmd0          | std_ulogic_vector | x"40" & x"00" & x"00" & x"00" & x"00" & x"95" | Software reset                                |
| cmd55         | std_ulogic_vector | x"77" & x"00" & x"00" & x"00" & x"00" & x"ff" | Leading command of ACMD<n> command            |
| acmd41        | std_ulogic_vector | x"69" & x"40" & x"00" & x"00" & x"00" & x"ff" | For only SDC. Initiate initialization process |
| div_freq      | integer           | 200                                           |                                               |
| power_on_num  | integer           | 5000                                          |                                               |
| over_time_run | integer           | 25000                                         |                                               |
## Ports

| Port name    | Direction | Type      | Description |
| ------------ | --------- | --------- | ----------- |
| clk_ref      | in        | std_logic |             |
| rst_n        | in        | std_logic |             |
| sd_simo      | in        | std_logic |             |
| sd_clk       | out       | std_logic |             |
| sd_cs        | out       | std_logic |             |
| sd_mosi      | out       | std_logic |             |
| sd_init_done | out       | std_logic |             |
## Signals

| Name            | Type                           | Description |
| --------------- | ------------------------------ | ----------- |
| state           | sd_spi_init_state              |             |
| state_nxt       | sd_spi_init_state              |             |
| div_cnt         | unsigned                       |             |
| dived_clk       | std_logic                      |             |
| poweron_cnt     | unsigned                       |             |
| sd_resp_en      | std_logic                      |             |
| sd_resp_data    | std_logic_vector (47 downto 0) |             |
| sd_resp_flag    | std_logic                      |             |
| sd_resp_bit_cnt | std_logic_vector (5 downto 0)  |             |
| cmd_bit_cnt     | std_logic_vector (5 downto 0)  |             |
| overtime_cnt    | std_logic_vector (15 downto 0) |             |
| overtime_en     | std_logic                      |             |
| div_clk_neg     | std_logic                      |             |
## Types

| Name              | Type                                                                                                                                                                                                                                                                   | Description |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| sd_spi_init_state | (st_idle,<br><span style="padding-left:20px"> st_send_cmd0,<br><span style="padding-left:20px"> st_wait_cmd0,<br><span style="padding-left:20px"> st_send_cmd55,<br><span style="padding-left:20px"> st_send_acmd41,<br><span style="padding-left:20px"> st_init_done) |             |
