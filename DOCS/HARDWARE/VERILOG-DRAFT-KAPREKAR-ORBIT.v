module kaprekar_orbit #(
    parameter WIDTH = 16,
    parameter MAX_STEPS = 20
) (
    input clk,
    input reset,
    input signed [WIDTH-1:0] p0,
    input signed [WIDTH-1:0] q0,
    output reg signed [WIDTH-1:0] p_out,
    output reg signed [WIDTH-1:0] q_out,
    output reg converged
);
    reg signed [WIDTH-1:0] p_reg, q_reg;
    reg [4:0] step;
    
    wire signed [WIDTH-1:0] next_state;
    
    tropical_envelope #(.WIDTH(WIDTH)) env (
        .p(p_reg),
        .q(q_reg),
        .next_state(next_state)
    );
    
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            p_reg <= p0;
            q_reg <= q0;
            step <= 0;
            converged <= 0;
        end else if (step < MAX_STEPS && !converged) begin
            p_reg <= next_state;  // Simplified for demo (extend for p/q pair)
            q_reg <= next_state;  // Adjust per full envelope
            step <= step + 1;
            
            if (p_reg == next_state && q_reg == next_state) begin
                converged <= 1;
            end
        end
    end
    
    assign p_out = p_reg;
    assign q_out = q_reg;
endmodule
