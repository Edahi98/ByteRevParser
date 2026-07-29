export const DEFAULT_MODEL_PARAMS = {
  ngramMin: 3,
  ngramMax: 5,
  maxFeatures: 20000,
  bottleneckDim: 100,
  epochs: 15,
  kMin: 2,
  kMax: 15,
  contaminationPercent: 5,
}

export function toConfigOverrides(params) {
  return {
    tfidf: { ngram_range: [params.ngramMin, params.ngramMax], max_features: params.maxFeatures },
    autoencoder: { bottleneck_dim: params.bottleneckDim, epochs: params.epochs },
    clustering: { k_min: params.kMin, k_max: params.kMax },
    novelty: { contamination: params.contaminationPercent / 100 },
  }
}
