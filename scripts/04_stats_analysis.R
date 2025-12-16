# Packages
library(ggplot2)
library(dplyr)
library(rstatix)

# 1️⃣ Lecture des données
df <- read.csv("data/processed/gc_genomes.csv")
df$genus <- as.factor(df$genus)

# 2️⃣ Statistiques descriptives
desc <- df %>%
  group_by(genus) %>%
  summarise(
    mean_gc = mean(gc_content_percent),
    sd_gc = sd(gc_content_percent),
    n = n()
  )
print(desc)

# 3️⃣ Test de normalité par genre
norm_test <- df %>%
  group_by(genus) %>%
  summarise(shapiro_p = shapiro.test(gc_content_percent)$p.value)
print(norm_test)

# 4️⃣ Choix du test
if(all(norm_test$shapiro_p > 0.05)){
  test <- aov(gc_content_percent ~ genus, data=df)
  summary(test)
  posthoc <- TukeyHSD(test)
  print(posthoc)
} else {
  test <- kruskal_test(gc_content_percent ~ genus, data=df)
  print(test)
  posthoc <- df %>%
    dunn_test(gc_content_percent ~ genus, p.adjust.method = "bonferroni")
  print(posthoc)
}

# 5️⃣ Visualisation
p <- ggplot(df, aes(x=genus, y=gc_content_percent, color=genus)) +
  geom_boxplot(outlier.shape = NA) +
  geom_jitter(width=0.2, alpha=0.6) +
  theme_minimal() +
  labs(
    title="%GC content par genre",
    x="Genre",
    y="%GC"
  ) +
  theme(
    plot.title = element_text(color="white"),
    axis.title.x = element_text(color="white"),
    axis.title.y = element_text(color="white"),
    axis.text.x = element_text(color="white"),
    axis.text.y = element_text(color="white"),
    legend.title = element_text(color="white"),
    legend.text = element_text(color="white")
  )
# 6️⃣ Sauvegarde figure
ggsave("figures/gc_content_boxplot.png", plot=p, width=6, height=4, dpi=300)
