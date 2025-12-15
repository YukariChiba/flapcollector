<template>
  <div class="row g-3">
    <!-- API Query Params -->
    <div class="col-7">
      <BCard class="h-100 mb-0" body-class="p-3">
        <span
          class="d-block small text-uppercase text-muted mb-2 ls-1"
          style="letter-spacing: 1px; font-size: 0.75rem"
        >
          Query Parameters
        </span>
        <div class="d-flex gap-2">
          <BInputGroup prepend="Votes &geq;" size="sm" class="w-auto">
            <BFormInput
              type="number"
              min="1"
              :model-value="modelValue.votes"
              @update:model-value="(v) => updateParam('votes', Number(v))"
            />
          </BInputGroup>
          <BInputGroup prepend="Current Rate &geq;" size="sm" class="w-auto">
            <BFormInput
              type="number"
              min="0"
              :model-value="modelValue.current_rate"
              @update:model-value="(v) => updateParam('current_rate', Number(v))"
            />
          </BInputGroup>
        </div>
      </BCard>
    </div>
    <div class="col-5">
      <BCard class="h-100 mb-0" body-class="p-3">
        <span
          class="d-block small text-uppercase text-muted mb-2 ls-1"
          style="letter-spacing: 1px; font-size: 0.75rem"
        >
          Filter Parameters
        </span>
        <div class="d-flex gap-2">
          <BInputGroup prepend="Average Rate &geq;" size="sm" class="w-auto">
            <BFormInput
              type="number"
              min="0"
              step="0.1"
              :model-value="modelValue.average_rate"
              @update:model-value="(v) => updateParam('average_rate', Number(v))"
            />
          </BInputGroup>
        </div>
      </BCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { FilterState } from '../types'
import { BCard, BInputGroup, BFormInput } from 'bootstrap-vue-next'

const props = defineProps<{ modelValue: FilterState }>()
const emit = defineEmits<{ 'update:modelValue': [value: FilterState] }>()

const updateParam = (key: 'votes' | 'average_rate' | 'current_rate', val: number) => {
  emit('update:modelValue', { ...props.modelValue, [key]: val })
}
</script>
