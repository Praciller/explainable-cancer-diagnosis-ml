import contract from "./showcase_contract.json";
import type { EvaluationReport, ModelInfo } from "../types/api";

export const SHOWCASE_MODEL_INFO = contract.model_info as ModelInfo;
export const SHOWCASE_EVALUATION = contract.evaluation as EvaluationReport;
