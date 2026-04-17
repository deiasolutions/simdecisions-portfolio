# SPEC-MLTRAIN-01: Model Registry and Prediction Tracking

## Priority
P2

## Model Assignment
sonnet

## Depends On
LEDGER-01

## Intent
Create the database schema for ML model registry, predictions, and preference pairs. Implement prediction tracking API (make prediction + resolve with ground truth). This is the foundation for ML training pipeline - storage and tracking only, no actual model training yet.

## Files to Read First
.deia/BOOT.md
hivenode/main.py

## Acceptance Criteria
- [ ] `ml_models` table created with fields: id, name, version, model_type, trained_at, training_events_count, architecture (JSONB), feature_schema (JSONB), metrics (JSONB), artifact_path, status, is_active, parent_model_id, created_at, created_by
- [ ] `ml_predictions` table created with fields: id, model_id, prediction_type, input_event_id, input_features (JSONB), prediction (JSONB), confidence, actual_outcome (JSONB), outcome_event_id, was_correct, error_magnitude, predicted_at, resolved_at
- [ ] `ml_preference_pairs` table created with fields: id, model_domain, chosen_event_id, rejected_event_id, chosen_content_hash, rejected_content_hash, feedback_text, judge_type, judge_id, confidence, created_at
- [ ] `ml_datasets` table created with fields: id, name, dataset_type, row_count, feature_count, events_from, events_to, artifact_path, version, created_at
- [ ] Proper indexes on all tables (model_id, user_id, timestamps, is_active)
- [ ] Prediction service with `make_prediction()` method that stores prediction and returns prediction_id
- [ ] Prediction service with `resolve_prediction()` method that records ground truth and calculates was_correct
- [ ] Model registry with `register_model()` method that stores model metadata
- [ ] Model registry with `get_active_model(model_type)` method that returns current active version
- [ ] Migration creates all tables idempotently
- [ ] At least 4 unit tests for prediction tracking (make + resolve lifecycle)
- [ ] At least 2 unit tests for model registry operations
- [ ] Schema compatible with PostgreSQL and SQLite
- [ ] No file over 500 lines

## Constraints
- This spec implements ONLY schema and tracking APIs
- Model training pipeline is NOT in scope
- Feature extraction is NOT in scope
- Actual ML model execution is NOT in scope (just tracking infrastructure)
- Drift detection is NOT in scope
- Use SQLAlchemy Core pattern
- All file paths absolute
- No stubs
- No git operations

## Smoke Test
After completion:
1. Register a test model with model_type="effort_surrogate"
2. Make a prediction with input_features and get prediction_id
3. Resolve prediction with actual_outcome
4. Query prediction record - verify was_correct is calculated
5. Get active model for "effort_surrogate" - verify correct model returned
6. List all predictions - verify stored correctly
