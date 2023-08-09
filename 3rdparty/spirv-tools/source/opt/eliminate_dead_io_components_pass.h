// Copyright (c) 2022 The Khronos Group Inc.
// Copyright (c) 2022 LunarG Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef SOURCE_OPT_ANALYZE_LIVE_INPUT_H_
#define SOURCE_OPT_ANALYZE_LIVE_INPUT_H_

#include <unordered_set>

#include "source/opt/pass.h"

namespace spvtools {
namespace opt {

// See optimizer.hpp for documentation.
<<<<<<<< HEAD:3rdparty/spirv-tools/source/opt/analyze_live_input_pass.h
class AnalyzeLiveInputPass : public Pass {
 public:
  explicit AnalyzeLiveInputPass(std::unordered_set<uint32_t>* live_locs,
                                std::unordered_set<uint32_t>* live_builtins)
      : live_locs_(live_locs), live_builtins_(live_builtins) {}

  const char* name() const override { return "analyze-live-input"; }
========
class EliminateDeadIOComponentsPass : public Pass {
 public:
  explicit EliminateDeadIOComponentsPass(spv::StorageClass elim_sclass,
                                         bool safe_mode = true)
      : elim_sclass_(elim_sclass), safe_mode_(safe_mode) {}

  const char* name() const override {
    return "eliminate-dead-input-components";
  }
>>>>>>>> github/master:3rdparty/spirv-tools/source/opt/eliminate_dead_io_components_pass.h
  Status Process() override;

  // Return the mask of preserved Analyses.
  IRContext::Analysis GetPreservedAnalyses() override {
    return IRContext::kAnalysisDefUse |
           IRContext::kAnalysisInstrToBlockMapping |
           IRContext::kAnalysisCombinators | IRContext::kAnalysisCFG |
           IRContext::kAnalysisDominatorAnalysis |
           IRContext::kAnalysisLoopAnalysis | IRContext::kAnalysisNameMap |
           IRContext::kAnalysisConstants | IRContext::kAnalysisTypes;
  }

 private:
<<<<<<<< HEAD:3rdparty/spirv-tools/source/opt/analyze_live_input_pass.h
  // Do live input analysis
  Status DoLiveInputAnalysis();

  std::unordered_set<uint32_t>* live_locs_;
  std::unordered_set<uint32_t>* live_builtins_;
========
  // Find the max constant used to index the variable declared by |var|
  // through OpAccessChain or OpInBoundsAccessChain. If any non-constant
  // indices or non-Op*AccessChain use of |var|, return |original_max|.
  unsigned FindMaxIndex(const Instruction& var, const unsigned original_max,
                        const bool skip_first_index = false);

  // Change the length of the array |inst| to |length|
  void ChangeArrayLength(Instruction& inst, unsigned length);

  // Change the length of the struct in |io_var| to |length|. |io_var|
  // is either the struct or a per-vertex-array of the struct.
  void ChangeIOVarStructLength(Instruction& io_var, unsigned length);

  // Storage class to be optimized. Must be Input or Output.
  spv::StorageClass elim_sclass_;

  // Only make changes that will not cause interface incompatibility if done
  // standalone. Currently this is only Input variables in vertex shaders.
  bool safe_mode_;
>>>>>>>> github/master:3rdparty/spirv-tools/source/opt/eliminate_dead_io_components_pass.h
};

}  // namespace opt
}  // namespace spvtools

#endif  // SOURCE_OPT_ANALYZE_LIVE_INPUT_H_
