
module multibank # (
  DATA_WIDTH = 32,
  ADDR_WIDTH= 8,
  NUM_BANKS=2
)(
#<RW_PORTS
    clk,
    addr,
    din,
    csb,
    web,
    dout
#>RW_PORTS
#<R_PORTS
    clk,
    addr,
    csb,
    web,
    dout
#>R_PORTS
  );

  parameter RAM_DEPTH = 1 << ADDR_WIDTH;
  parameter BANK_SEL = (NUM_BANKS <= 2)? 1 :
                       (NUM_BANKS <= 4)? 2 :
                       (NUM_BANKS <= 8)? 3 :
                       (NUM_BANKS <= 16)? 4 : 5;

  input clk;
  input [ADDR_WIDTH -1 : 0] addr;
  input [DATA_WIDTH - 1: 0] din;
  input csb;
  input web;
  output reg [DATA_WIDTH - 1 : 0] dout;

#!PORT_NUM!0#
#<BANK_DEFS
  reg csb#$PORT_NUM$#;
  reg web#$PORT_NUM$#;
  reg [DATA_WIDTH - 1 : 0] dout#$PORT_NUM$#;
#!PORT_NUM!PORT_NUM+1#
#>BANK_DEFS

#!PORT_NUM!0#
#<BANK_INIT
  bank #(DATA_WIDTH, ADDR_WIDTH) bank#$PORT_NUM$# (
#<BANK_RW_PORTS
    .clk(clk),
    .addr(addr[ADDR_WIDTH - BANK_SEL - 1 : 0]),
    .din(din),
    .csb(csb#$PORT_NUM$#),
    .web(web#$PORT_NUM$#),
    .dout(dout#$PORT_NUM$#)
#!PORT_NUM!PORT_NUM+1#
#>BANK_RW_PORTS
  );
#>BANK_INIT

always @(posedge clk) begin
    case (addr[ADDR_WIDTH - 1 : ADDR_WIDTH - BANK_SEL])
#!PORT_NUM!0#
#<BANK_CASE
        #$PORT_NUM$#: begin
            dout <= dout#$PORT_NUM$#;
            web#$PORT_NUM$# <= web;
        end
#!PORT_NUM!PORT_NUM+1#
#>BANK_CASE
    endcase
end

endmodule
