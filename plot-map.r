library('tidyverse')
library('sf')

# Spatially join selected blocks and block groups 
df <- read_csv('results/2014/clf_selected_blocks.csv')
df.geo <- st_read('data/block-groups.geojson')
df <- df %>% mutate(GEOID = factor(GEOID), label = factor(label))
df.geo <- df.geo %>% filter(grepl('^42101', GEOID))
df <- left_join(df.geo, df)

# Create map 
ggplot(df) +
    geom_sf(aes(fill = label)) +
    ggtitle("Best Classifier: Top 14% Predictions - 2014")
ggsave('results/2014/map.png', dpi=150)

