# ShiftCenter ML Training Specification

**Spec ID:** SPEC-ML-TRAINING-V1
**Created:** 2026-04-06
**Status:** DRAFT
**Depends On:** SPEC-EVENT-LEDGER-GAMIFICATION, SPEC-GAMIFICATION-V1
**Ships With:** V1.0
**Priority:** P3

---

## Acceptance Criteria

- [ ] Data collection pipeline captures events as training data
- [ ] Database schema supports model metadata and training runs
- [ ] At least one surrogate model type trainable end-to-end
- [ ] Prediction service returns inference results via API
- [ ] Training pipeline orchestrated and repeatable

---

## Executive Summary

Pillar 3: AI Training. From day one, not deferred.

Every event in ShiftCenter is training data. Every user action teaches the system. Every prediction is validated against ground truth. The platform learns as it runs.

### Core Principle

> **The simulation is the factory. The surrogates are the product. The ledger is the quality record.**

We don't bolt ML on later. We architect for learning from the first commit.

---

## 1. Three Pillars Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         EVENT LEDGER                                     │
│                    (Single Source of Truth)                              │
└─────────────────────────────────────────────────────────────────────────┘
         │                      │                      │
         ▼                      ▼                      ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   PILLAR 1      │  │   PILLAR 2      │  │   PILLAR 3      │
│   Core App      │  │   Gamification  │  │   AI Training   │
│                 │  │                 │  │                 │
│ • Wiki          │  │ • XP/Levels     │  │ • Surrogates    │
│ • Notebooks     │  │ • Badges        │  │ • Preference    │
│ • Eggs          │  │ • Streaks       │  │ • Prediction    │
│ • Tasks         │  │ • Path Map      │  │ • Embeddings    │
│ • Deploys       │  │ • ρ-π-σ-τ       │  │ • Calibration   │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                ▼
                    ┌─────────────────────┐
                    │   FEEDBACK LOOP     │
                    │                     │
                    │ AI improves → App   │
                    │ App emits → Ledger  │
                    │ Ledger feeds → AI   │
                    └─────────────────────┘
```

---

## 2. Data Collection Strategy

### 2.1 Collection Points

| Collection Point | Events | ML Use Case |
|------------------|--------|-------------|
| **Task lifecycle** | CREATED → DISPATCHED → COMPLETED → APPROVED/REJECTED | Effort estimation, approval prediction, RLHF |
| **Code review** | REVIEW_STARTED → BUG_CAUGHT → REVIEW_COMPLETED | Defect prediction |
| **Wiki activity** | PAGE_CREATED → PAGE_LINKED → PAGE_VIEWED | Content quality scoring |
| **User behavior** | SESSION_* → factor changes → path choices | User modeling, recommendations |
| **Search** | SEARCH_EXECUTED → SEARCH_CLICKED | Search ranking |
| **Specs** | SPEC_CREATED → SPEC_APPROVED → SPEC_SHIPPED | Spec success prediction |
| **Deploys** | DEPLOY_STARTED → DEPLOY_COMPLETED/FAILED | Deployment risk |

### 2.2 What Makes Good Training Data

| Signal Type | Example | Value |
|-------------|---------|-------|
| **Preference pairs** | Task A approved, Task B rejected | RLHF gold |
| **Predicted vs actual** | Estimated 3h, took 5h | Calibration |
| **Implicit feedback** | Page viewed 10x, never edited | Quality signal |
| **Explicit feedback** | Rejection reason: "incomplete" | Labeled data |
| **Sequential patterns** | User always does X after Y | Behavior model |
| **Counterfactuals** | Same task, different bee, different outcome | Causal learning |

### 2.3 Collection Rules

```python
# Every event automatically collected
# These annotations mark ML-relevant fields

@ml_feature("effort_estimation")
class TaskCreatedContext:
    estimated_hours: float
    spec_word_count: int
    spec_complexity_score: float
    dependencies_count: int
    
@ml_label("effort_estimation")  
class TaskCompletedContext:
    actual_duration_ms: int
    
@ml_preference_pair("approval_model")
class TaskApprovedContext:
    task_output_hash: str
    preferred: bool = True
    
@ml_preference_pair("approval_model")
class TaskRejectedContext:
    task_output_hash: str
    preferred: bool = False
    feedback: str
```

---

## 3. Database Schema

### 3.1 Model Registry

```sql
CREATE TABLE ml_models (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Identity
    name VARCHAR(100) NOT NULL,
    version VARCHAR(20) NOT NULL,
    model_type VARCHAR(50) NOT NULL,
    
    -- Training metadata
    trained_at TIMESTAMPTZ,
    training_started_at TIMESTAMPTZ,
    training_events_count INTEGER,
    training_events_from TIMESTAMPTZ,
    training_events_to TIMESTAMPTZ,
    
    -- Architecture
    architecture JSONB DEFAULT '{}',      -- {"type": "xgboost", "params": {...}}
    feature_schema JSONB DEFAULT '{}',    -- Input feature names and types
    output_schema JSONB DEFAULT '{}',     -- Output structure
    
    -- Performance metrics
    metrics JSONB DEFAULT '{}',
    validation_set_size INTEGER,
    
    -- Storage
    artifact_path VARCHAR(500),
    artifact_size_bytes INTEGER,
    
    -- Status
    status VARCHAR(20) DEFAULT 'training',
    is_active BOOLEAN DEFAULT FALSE,
    promoted_at TIMESTAMPTZ,
    retired_at TIMESTAMPTZ,
    
    -- Lineage
    parent_model_id UUID REFERENCES ml_models(id),
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    
    UNIQUE(name, version)
);

CREATE INDEX idx_ml_models_active ON ml_models(name) WHERE is_active = TRUE;
CREATE INDEX idx_ml_models_type ON ml_models(model_type);
```

### 3.2 Training Datasets

```sql
CREATE TABLE ml_datasets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    name VARCHAR(100) NOT NULL,
    dataset_type VARCHAR(50) NOT NULL,    -- 'preference_pairs', 'regression', 'classification'
    
    -- Source
    source_query TEXT,                     -- Query used to extract from ledger
    event_kinds JSONB DEFAULT '[]',
    
    -- Stats
    row_count INTEGER,
    feature_count INTEGER,
    label_distribution JSONB DEFAULT '{}',
    
    -- Time bounds
    events_from TIMESTAMPTZ,
    events_to TIMESTAMPTZ,
    
    -- Storage
    artifact_path VARCHAR(500),
    
    -- Versioning
    version INTEGER DEFAULT 1,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE ml_dataset_splits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    dataset_id UUID REFERENCES ml_datasets(id),
    split_type VARCHAR(20) NOT NULL,       -- 'train', 'validation', 'test', 'holdout'
    
    row_count INTEGER,
    row_ids JSONB DEFAULT '[]',            -- Event IDs in this split
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 3.3 Predictions

```sql
CREATE TABLE ml_predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    model_id UUID REFERENCES ml_models(id),
    
    -- What was predicted
    prediction_type VARCHAR(50) NOT NULL,
    input_event_id UUID,
    input_features JSONB NOT NULL,
    
    -- Prediction output
    prediction JSONB NOT NULL,
    confidence FLOAT,
    explanation JSONB,                     -- SHAP values, feature importance
    
    -- Ground truth (filled in when available)
    actual_outcome JSONB,
    outcome_event_id UUID,
    outcome_timestamp TIMESTAMPTZ,
    
    -- Evaluation
    was_correct BOOLEAN,
    error_magnitude FLOAT,                 -- For regression
    
    -- Timing
    predicted_at TIMESTAMPTZ DEFAULT NOW(),
    resolved_at TIMESTAMPTZ,
    resolution_latency_ms INTEGER GENERATED ALWAYS AS (
        EXTRACT(EPOCH FROM (resolved_at - predicted_at)) * 1000
    ) STORED
);

CREATE INDEX idx_ml_predictions_model ON ml_predictions(model_id);
CREATE INDEX idx_ml_predictions_unresolved ON ml_predictions(model_id) 
    WHERE actual_outcome IS NULL;
CREATE INDEX idx_ml_predictions_time ON ml_predictions(predicted_at DESC);
```

### 3.4 Preference Pairs (RLHF)

```sql
CREATE TABLE ml_preference_pairs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    model_domain VARCHAR(50) NOT NULL,     -- 'task_approval', 'content_quality'
    
    -- The pair
    chosen_event_id UUID NOT NULL,
    rejected_event_id UUID,                -- NULL for absolute ratings
    
    -- Content hashes for deduplication
    chosen_content_hash VARCHAR(64),
    rejected_content_hash VARCHAR(64),
    
    -- Feedback
    feedback_text TEXT,
    feedback_categories JSONB DEFAULT '[]',
    
    -- Source
    judge_type VARCHAR(20) NOT NULL,       -- 'human', 'model', 'implicit'
    judge_id UUID,
    
    -- Quality
    confidence FLOAT,
    is_verified BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_preference_pairs_domain ON ml_preference_pairs(model_domain);
```

### 3.5 User Embeddings

```sql
CREATE TABLE ml_user_embeddings (
    user_id UUID PRIMARY KEY REFERENCES users(id),
    
    -- Embedding vector
    embedding VECTOR(128),
    
    -- Metadata
    events_count INTEGER,
    events_from TIMESTAMPTZ,
    events_to TIMESTAMPTZ,
    
    -- Model info
    model_id UUID REFERENCES ml_models(id),
    model_version VARCHAR(20),
    
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_user_embeddings_vector ON ml_user_embeddings 
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

---

## 4. Model Types

### 4.1 Effort Surrogate

**Purpose:** Predict how long a task will take.

```python
class EffortSurrogate:
    """
    Predicts task duration from spec features.
    """
    
    INPUT_FEATURES = [
        "spec_word_count",
        "spec_code_blocks",
        "dependencies_count",
        "estimated_complexity",      # From spec frontmatter
        "similar_tasks_avg_duration", # Historical
        "assigned_model",            # sonnet vs opus vs haiku
        "user_rho",                  # Reliability factor
        "user_pi",                   # Productivity factor
        "hour_of_day",
        "day_of_week"
    ]
    
    OUTPUT = {
        "predicted_hours": float,
        "confidence_interval": (float, float),
        "similar_tasks": List[str]
    }
    
    TRAINING_SIGNAL = "TASK_COMPLETED.actual_duration_ms"
```

### 4.2 Approval Predictor

**Purpose:** Predict whether a task output will be approved.

```python
class ApprovalPredictor:
    """
    Predicts P(approved) for task output.
    """
    
    INPUT_FEATURES = [
        "output_word_count",
        "output_code_ratio",
        "spec_coverage_score",       # How much of spec addressed
        "test_pass_rate",
        "lint_errors",
        "similar_outputs_approval_rate",
        "user_sigma",                # Sophistication factor
        "bee_model",
        "time_of_day"
    ]
    
    OUTPUT = {
        "p_approved": float,
        "risk_factors": List[str],
        "suggested_improvements": List[str]
    }
    
    TRAINING_SIGNAL = "TASK_APPROVED | TASK_REJECTED"
```

### 4.3 Content Quality Scorer

**Purpose:** Score wiki page quality.

```python
class ContentQualityScorer:
    """
    Scores wiki page quality 0-100.
    """
    
    INPUT_FEATURES = [
        "word_count",
        "has_frontmatter",
        "has_code_blocks",
        "outbound_links_count",
        "readability_score",
        "structure_score",           # Headers, sections
        "author_tau",                # Teaching factor
    ]
    
    OUTPUT = {
        "quality_score": int,        # 0-100
        "strengths": List[str],
        "improvements": List[str]
    }
    
    TRAINING_SIGNAL = [
        "PAGE_LINKED (backlinks as quality proxy)",
        "PAGE_VIEWED (views as engagement proxy)",
        "PAGE_UPDATED (edits as incompleteness signal)"
    ]
```

### 4.4 Defect Detector

**Purpose:** Predict if code has bugs before review.

```python
class DefectDetector:
    """
    Predicts P(has_defect) for code changes.
    """
    
    INPUT_FEATURES = [
        "lines_changed",
        "files_changed",
        "complexity_delta",
        "test_coverage_delta",
        "author_history_defect_rate",
        "file_history_defect_rate",
        "time_since_last_change",
        "is_friday_deploy"           # Classic
    ]
    
    OUTPUT = {
        "p_defect": float,
        "risk_files": List[str],
        "suggested_review_focus": List[str]
    }
    
    TRAINING_SIGNAL = "BUG_CAUGHT"
```

### 4.5 Path Recommender

**Purpose:** Suggest next skill/node in path map.

```python
class PathRecommender:
    """
    Recommends next best skill based on user profile.
    """
    
    INPUT_FEATURES = [
        "rho", "pi", "sigma", "tau",
        "current_skills",
        "recent_events",
        "time_since_last_unlock",
        "xp_velocity",
        "streak_length"
    ]
    
    OUTPUT = {
        "recommended_skills": List[str],
        "reasons": List[str],
        "estimated_time_to_unlock": List[int]
    }
    
    TRAINING_SIGNAL = "SKILL_UNLOCKED patterns"
```

### 4.6 User Embedding Model

**Purpose:** Learn dense representation of user behavior.

```python
class UserEmbedder:
    """
    Embeds user event history into 128-dim vector.
    """
    
    INPUT = "Sequence of user events (last 1000)"
    
    OUTPUT = {
        "embedding": List[float],    # 128-dim
    }
    
    USES = [
        "Similar user discovery",
        "Cold start recommendations",
        "Anomaly detection",
        "Cohort analysis"
    ]
    
    ARCHITECTURE = "Transformer encoder on event sequences"
```

### 4.7 Spec Success Predictor

**Purpose:** Predict if a spec will ship successfully.

```python
class SpecSuccessPredictor:
    """
    Predicts P(spec ships successfully).
    """
    
    INPUT_FEATURES = [
        "spec_word_count",
        "spec_sections_count",
        "has_acceptance_criteria",
        "has_migration_plan",
        "dependencies_count",
        "similar_specs_success_rate",
        "author_sigma",
        "estimated_tasks"
    ]
    
    OUTPUT = {
        "p_success": float,
        "risk_factors": List[str],
        "suggested_additions": List[str]
    }
    
    TRAINING_SIGNAL = "SPEC_SHIPPED vs SPEC_ABANDONED"
```

---

## 5. Training Pipeline

### 5.1 Pipeline Architecture

```
┌─────────────────┐
│  Event Ledger   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Extractor │ ── Queries ledger, builds datasets
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Feature Engine  │ ── Transforms raw events to features
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Split Manager  │ ── Train/val/test/holdout splits
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Trainer      │ ── Fits model, logs metrics
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Validator     │ ── Evaluates on holdout
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Registry      │ ── Stores model, tracks lineage
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Promoter      │ ── A/B test, promote to active
└─────────────────┘
```

### 5.2 Training Service

```python
# services/ml/training_service.py

class TrainingService:
    
    async def train_model(
        self,
        model_type: str,
        config: TrainingConfig
    ) -> MLModel:
        """
        Full training pipeline.
        """
        
        # 1. Extract dataset
        dataset = await self.data_extractor.extract(
            model_type=model_type,
            events_from=config.events_from,
            events_to=config.events_to
        )
        
        # 2. Feature engineering
        features = await self.feature_engine.transform(
            dataset=dataset,
            feature_config=MODEL_FEATURES[model_type]
        )
        
        # 3. Split
        splits = self.split_manager.split(
            features=features,
            train_ratio=0.7,
            val_ratio=0.15,
            test_ratio=0.1,
            holdout_ratio=0.05
        )
        
        # 4. Train
        model = self.trainer.fit(
            model_type=model_type,
            train_data=splits.train,
            val_data=splits.validation,
            config=config
        )
        
        # 5. Validate
        metrics = self.validator.evaluate(
            model=model,
            test_data=splits.test
        )
        
        # 6. Register
        registered = await self.registry.register(
            model=model,
            metrics=metrics,
            dataset_id=dataset.id,
            config=config
        )
        
        # 7. Emit event
        await self.emit_event(
            kind="MODEL_TRAINED",
            target_id=registered.id,
            context={
                "model_name": model_type,
                "version": registered.version,
                "metrics": metrics,
                "training_events": dataset.row_count
            }
        )
        
        return registered
    
    async def collect_preference_pairs(
        self,
        domain: str,
        since: datetime
    ) -> List[PreferencePair]:
        """
        Extract RLHF pairs from approval/rejection events.
        """
        
        if domain == "task_approval":
            approved = await self.ledger.get_events(
                kind="TASK_APPROVED",
                since=since
            )
            rejected = await self.ledger.get_events(
                kind="TASK_REJECTED",
                since=since
            )
            
            pairs = []
            
            for event in approved:
                pairs.append(PreferencePair(
                    domain=domain,
                    chosen_event_id=event.id,
                    chosen_content_hash=hash(event.context["output"]),
                    judge_type="human",
                    judge_id=event.actor.id
                ))
            
            for event in rejected:
                # Find the corrected version if exists
                correction = await self.find_correction(event)
                
                pairs.append(PreferencePair(
                    domain=domain,
                    chosen_event_id=correction.id if correction else None,
                    rejected_event_id=event.id,
                    rejected_content_hash=hash(event.context["output"]),
                    feedback_text=event.context.get("feedback"),
                    judge_type="human",
                    judge_id=event.actor.id
                ))
            
            return pairs
```

### 5.3 Continuous Training

```python
# services/ml/continuous_trainer.py

class ContinuousTrainer:
    """
    Runs on schedule, retrains models as data accumulates.
    """
    
    RETRAIN_TRIGGERS = {
        "effort_surrogate": {
            "min_new_events": 100,
            "max_age_days": 7,
            "performance_threshold": 0.05  # Retrain if error increases 5%
        },
        "approval_predictor": {
            "min_new_events": 50,
            "max_age_days": 3,
            "performance_threshold": 0.03
        }
    }
    
    async def check_and_retrain(self):
        """
        Check all models, retrain if needed.
        """
        for model_type, triggers in self.RETRAIN_TRIGGERS.items():
            active_model = await self.registry.get_active(model_type)
            
            if not active_model:
                # No active model, train from scratch
                await self.training_service.train_model(model_type)
                continue
            
            # Check triggers
            should_retrain = await self.should_retrain(
                model=active_model,
                triggers=triggers
            )
            
            if should_retrain:
                new_model = await self.training_service.train_model(
                    model_type=model_type,
                    config=TrainingConfig(
                        events_from=active_model.training_events_to,
                        incremental=True,
                        parent_model_id=active_model.id
                    )
                )
                
                # A/B test before promotion
                await self.ab_test_and_promote(active_model, new_model)
```

---

## 6. Prediction Service

### 6.1 Real-Time Predictions

```python
# services/ml/prediction_service.py

class PredictionService:
    
    async def predict(
        self,
        model_type: str,
        features: dict,
        source_event_id: str = None
    ) -> Prediction:
        """
        Make prediction and track for resolution.
        """
        
        model = await self.registry.get_active(model_type)
        
        if not model:
            raise NoActiveModelError(model_type)
        
        # Make prediction
        result = model.predict(features)
        
        # Store for later resolution
        prediction_record = await self.db.insert(MLPrediction(
            model_id=model.id,
            prediction_type=model_type,
            input_event_id=source_event_id,
            input_features=features,
            prediction=result.value,
            confidence=result.confidence,
            explanation=result.explanation
        ))
        
        # Emit event
        await self.emit_event(
            kind="PREDICTION_MADE",
            context={
                "model_type": model_type,
                "model_version": model.version,
                "confidence": result.confidence,
                "prediction_id": prediction_record.id
            }
        )
        
        return Prediction(
            id=prediction_record.id,
            value=result.value,
            confidence=result.confidence,
            explanation=result.explanation
        )
    
    async def resolve(
        self,
        prediction_id: str,
        actual_outcome: dict,
        outcome_event_id: str
    ):
        """
        Record ground truth when available.
        """
        
        prediction = await self.db.get(prediction_id)
        
        # Evaluate correctness
        was_correct, error = self.evaluate(
            prediction.prediction,
            actual_outcome,
            prediction.prediction_type
        )
        
        # Update record
        prediction.actual_outcome = actual_outcome
        prediction.outcome_event_id = outcome_event_id
        prediction.was_correct = was_correct
        prediction.error_magnitude = error
        prediction.resolved_at = datetime.utcnow()
        
        await self.db.update(prediction)
        
        # Emit event
        await self.emit_event(
            kind="PREDICTION_RESOLVED",
            context={
                "prediction_id": prediction_id,
                "model_id": prediction.model_id,
                "was_correct": was_correct,
                "error_magnitude": error,
                "confidence": prediction.confidence,
                "resolution_latency_ms": prediction.resolution_latency_ms
            }
        )
```

### 6.2 Batch Predictions

```python
async def predict_batch(
    self,
    model_type: str,
    feature_batch: List[dict]
) -> List[Prediction]:
    """
    Efficient batch prediction.
    """
    
    model = await self.registry.get_active(model_type)
    
    # Vectorized prediction
    results = model.predict_batch(feature_batch)
    
    # Store all predictions
    records = await self.db.insert_batch([
        MLPrediction(
            model_id=model.id,
            prediction_type=model_type,
            input_features=features,
            prediction=result.value,
            confidence=result.confidence
        )
        for features, result in zip(feature_batch, results)
    ])
    
    return [
        Prediction(id=r.id, value=r.prediction, confidence=r.confidence)
        for r in records
    ]
```

---

## 7. Calibration & Monitoring

### 7.1 Calibration Tracking

```sql
CREATE VIEW model_calibration AS
SELECT 
    model_id,
    m.name as model_name,
    m.version as model_version,
    DATE_TRUNC('day', p.predicted_at) as day,
    
    -- Volume
    COUNT(*) as predictions,
    COUNT(p.actual_outcome) as resolved,
    
    -- Accuracy
    AVG(CASE WHEN p.was_correct THEN 1.0 ELSE 0.0 END) as accuracy,
    
    -- Calibration
    AVG(p.confidence) as avg_confidence,
    AVG(CASE WHEN p.was_correct THEN 1.0 ELSE 0.0 END) - AVG(p.confidence) as calibration_error,
    
    -- Resolution latency
    AVG(p.resolution_latency_ms) as avg_resolution_ms,
    
    -- Regression metrics (where applicable)
    AVG(p.error_magnitude) as mae,
    SQRT(AVG(p.error_magnitude ^ 2)) as rmse
    
FROM ml_predictions p
JOIN ml_models m ON p.model_id = m.id
WHERE p.actual_outcome IS NOT NULL
GROUP BY model_id, m.name, m.version, DATE_TRUNC('day', p.predicted_at);
```

### 7.2 Drift Detection

```python
class DriftDetector:
    """
    Detects feature drift and concept drift.
    """
    
    async def check_feature_drift(
        self,
        model_id: str,
        window_days: int = 7
    ) -> DriftReport:
        """
        Compare recent feature distributions to training distribution.
        """
        
        model = await self.registry.get(model_id)
        training_stats = model.feature_schema["distributions"]
        
        recent_predictions = await self.db.get_recent(
            model_id=model_id,
            days=window_days
        )
        
        recent_stats = self.compute_distributions(
            [p.input_features for p in recent_predictions]
        )
        
        drift_scores = {}
        for feature, train_dist in training_stats.items():
            recent_dist = recent_stats.get(feature)
            drift_scores[feature] = self.ks_test(train_dist, recent_dist)
        
        return DriftReport(
            model_id=model_id,
            drift_scores=drift_scores,
            significant_drift=[f for f, s in drift_scores.items() if s > 0.1]
        )
    
    async def check_concept_drift(
        self,
        model_id: str,
        window_days: int = 7
    ) -> ConceptDriftReport:
        """
        Check if model performance is degrading.
        """
        
        recent_calibration = await self.db.query(
            model_calibration,
            model_id=model_id,
            days=window_days
        )
        
        baseline = await self.get_baseline_performance(model_id)
        
        return ConceptDriftReport(
            model_id=model_id,
            baseline_accuracy=baseline.accuracy,
            recent_accuracy=recent_calibration.accuracy,
            drift_magnitude=baseline.accuracy - recent_calibration.accuracy,
            is_significant=abs(baseline.accuracy - recent_calibration.accuracy) > 0.05
        )
```

### 7.3 Alerting

```python
ALERT_RULES = {
    "accuracy_drop": {
        "condition": "accuracy < baseline - 0.1",
        "severity": "high",
        "action": "trigger_retrain"
    },
    "calibration_error": {
        "condition": "abs(calibration_error) > 0.15",
        "severity": "medium",
        "action": "notify"
    },
    "prediction_volume_drop": {
        "condition": "predictions < baseline * 0.5",
        "severity": "low",
        "action": "log"
    },
    "resolution_latency_spike": {
        "condition": "avg_resolution_ms > baseline * 2",
        "severity": "medium",
        "action": "notify"
    }
}
```

---

## 8. ρ-π-σ-τ Integration

### 8.1 Factors as Features

Every model can use user factors:

```python
def get_user_features(user_id: str) -> dict:
    """
    Extract user factors for model input.
    """
    
    factors = get_user_factors(user_id)
    
    return {
        # Raw factors
        "rho": factors.rho_normalized,
        "pi": factors.pi_normalized,
        "sigma": factors.sigma_normalized,
        "tau": factors.tau_normalized,
        
        # Derived
        "primary_factor": factors.primary_factor,
        "factor_balance": compute_balance(factors),  # Specialist vs generalist
        "factor_velocity": factors.recent_delta,     # Growing or stable
        
        # Historical
        "rho_30d_avg": factors.rho_history[-30:].mean(),
        "factor_trend": compute_trend(factors)       # Improving or declining
    }
```

### 8.2 Factor Prediction

```python
class FactorPredictor:
    """
    Predict future factor values.
    """
    
    async def predict_trajectory(
        self,
        user_id: str,
        days_ahead: int = 30
    ) -> FactorTrajectory:
        """
        Predict where user's factors will be in N days.
        """
        
        history = await self.get_factor_history(user_id, days=90)
        
        predictions = {}
        for factor in ["rho", "pi", "sigma", "tau"]:
            series = history[factor]
            predictions[factor] = self.forecast(series, days_ahead)
        
        return FactorTrajectory(
            user_id=user_id,
            current=history.current,
            predicted=predictions,
            confidence_intervals=self.compute_intervals(predictions)
        )
```

---

## 9. Event Emissions

### 9.1 ML-Specific Events

| Kind | When | Context |
|------|------|---------|
| `DATASET_CREATED` | New training dataset extracted | `row_count`, `event_kinds` |
| `MODEL_TRAINED` | Training complete | `metrics`, `training_events` |
| `MODEL_PROMOTED` | Model becomes active | `previous_model_id` |
| `MODEL_RETIRED` | Model deactivated | `reason`, `replacement_id` |
| `PREDICTION_MADE` | Prediction served | `model_type`, `confidence` |
| `PREDICTION_RESOLVED` | Ground truth recorded | `was_correct`, `error` |
| `DRIFT_DETECTED` | Feature or concept drift | `drift_type`, `magnitude` |
| `RETRAIN_TRIGGERED` | Automatic retrain started | `trigger_reason` |

### 9.2 Event Schema

```json
{
  "kind": "MODEL_TRAINED",
  "actor": {
    "id": "training_service",
    "type": "system"
  },
  "target": {
    "id": "model-uuid",
    "type": "model",
    "path": "effort_surrogate/1.2.0"
  },
  "context": {
    "model_name": "effort_surrogate",
    "version": "1.2.0",
    "training_events": 4500,
    "training_duration_ms": 45000,
    "metrics": {
      "mae": 0.45,
      "rmse": 0.62,
      "r2": 0.78
    },
    "parent_model_id": "previous-model-uuid"
  },
  "currencies": {
    "clock": 45000,
    "coin": 0.15,
    "carbon": 0.002
  }
}
```

---

## 10. API Endpoints

### 10.1 Model Registry

```
GET    /api/ml/models                     # List all models
GET    /api/ml/models/{id}                # Get model details
GET    /api/ml/models/{name}/active       # Get active version
POST   /api/ml/models/{id}/promote        # Promote to active
POST   /api/ml/models/{id}/retire         # Retire model
```

### 10.2 Predictions

```
POST   /api/ml/predict/{model_type}       # Make prediction
POST   /api/ml/predict/batch              # Batch predictions
POST   /api/ml/resolve/{prediction_id}    # Record outcome
GET    /api/ml/predictions                # List predictions
```

### 10.3 Training

```
POST   /api/ml/train/{model_type}         # Trigger training
GET    /api/ml/train/status/{job_id}      # Training status
GET    /api/ml/datasets                   # List datasets
POST   /api/ml/datasets/extract           # Extract new dataset
```

### 10.4 Monitoring

```
GET    /api/ml/calibration/{model_id}     # Calibration metrics
GET    /api/ml/drift/{model_id}           # Drift detection
GET    /api/ml/dashboard                  # Overall ML health
```

---

## 11. Dashboard Widget

### 11.1 ML Health Panel

```
┌─────────────────────────────────────────┐
│  ML System Health                       │
├─────────────────────────────────────────┤
│  Active Models: 6                       │
│  Predictions Today: 1,247               │
│  Avg Confidence: 0.82                   │
│  Resolution Rate: 94%                   │
│                                         │
│  ⚠️ effort_surrogate: drift detected   │
│  ✓ approval_predictor: healthy         │
│  ✓ quality_scorer: healthy             │
└─────────────────────────────────────────┘
```

### 11.2 Prediction Feed

```
┌─────────────────────────────────────────┐
│  Recent Predictions                     │
├─────────────────────────────────────────┤
│  MW-S04 effort: 2.5h (conf: 0.85)      │
│  └─ Actual: 2.8h ✓                     │
│                                         │
│  PR-127 defect: 0.23 (conf: 0.71)      │
│  └─ Pending review...                   │
│                                         │
│  SPEC-012 success: 0.91 (conf: 0.88)   │
│  └─ Pending ship...                     │
└─────────────────────────────────────────┘
```

---

## 12. Acceptance Criteria

### 12.1 Data Collection

- [ ] All relevant events captured with ML annotations
- [ ] Preference pairs extracted from approvals/rejections
- [ ] User factors (ρ-π-σ-τ) computed and updated
- [ ] Datasets extractable from ledger

### 12.2 Training

- [ ] Models trainable from extracted datasets
- [ ] Holdout validation enforced
- [ ] Model registry tracks lineage
- [ ] Continuous training triggers work

### 12.3 Prediction

- [ ] Real-time predictions served
- [ ] Predictions tracked for resolution
- [ ] Confidence scores provided
- [ ] Batch predictions efficient

### 12.4 Monitoring

- [ ] Calibration metrics computed
- [ ] Drift detection functional
- [ ] Alerts fire on degradation
- [ ] Dashboard shows ML health

### 12.5 Integration

- [ ] Models use ρ-π-σ-τ as features
- [ ] ML events emit to ledger
- [ ] Gamification can score ML events

---

## 13. Implementation Phases

### Phase 1: Foundation (Week 1-2)

- Schema: `ml_models`, `ml_predictions`, `ml_preference_pairs`
- Data extraction from ledger
- Prediction tracking (make + resolve)
- Basic model registry

### Phase 2: First Models (Week 3-4)

- Effort Surrogate (simplest, high value)
- Approval Predictor (RLHF foundation)
- Training pipeline
- Calibration views

### Phase 3: Monitoring (Week 5)

- Drift detection
- Alerting
- Dashboard widget
- Continuous training

### Phase 4: Advanced Models (Week 6+)

- Content Quality Scorer
- Defect Detector
- Path Recommender
- User Embeddings

---

## 14. Future Enhancements (V2+)

- **Online learning** — Update models incrementally without full retrain
- **A/B testing framework** — Formal experiment tracking
- **Explainability UI** — SHAP values, feature importance visualization
- **Custom model upload** — Users train their own models
- **Federated learning** — Learn across tenants without sharing data
- **AutoML** — Automatic feature engineering and model selection

---

**Spec Version:** 1.0
**Author:** Q88N × Claude
**Review Required:** ML infrastructure decisions before build
