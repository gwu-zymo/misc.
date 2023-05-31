# Define the start and end colors
start_color <- "red"
mid_color <- "green"
end_color <- "red"

# Generate a color gradient function
gradient_fun <- colorRampPalette(c(start_color, mid_color, end_color))

# Generate the color gradient
num_colors <- 100  # Number of colors in the gradient
colors <- gradient_fun(num_colors)

# Display the color gradient
image(1:num_colors, 1, as.matrix(1:num_colors), col = colors, xlab = "", ylab = "", xaxt = "n", yaxt = "n")

# Place a black dot
dot_position <- 10
points(dot_position, 1, pch = 19, col = "black")
