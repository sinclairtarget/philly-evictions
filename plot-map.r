library('tidyverse')
library('sf')

df <- read_csv('results/lr-block-groups.csv')
df.geo <- st_read('data/block-groups.geojson')

df <- df %>% mutate(GEOID = factor(GEOID), label = factor(label))
df.geo <- df.geo %>% filter(grepl('^42101', GEOID))

df <- left_join(df.geo, df)

ggplot(df) +
    geom_sf(aes(fill = label)) +
    theme(legend.position = 'none')
ggsave('map.png')
