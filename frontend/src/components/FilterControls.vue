<template>
  <div class="row g-3">
    <!-- Consensus Filter -->
    <div class="col-md-7 col-12">
      <BCard class="h-100 mb-0" body-class="p-3">
        <span
          class="d-block small text-uppercase text-muted mb-2 ls-1"
          style="letter-spacing: 1px; font-size: 0.75rem"
        >
          Consensus (Votes)
        </span>
        <BButtonGroup class="w-100">
          <BButton
            v-for="val in [1, 2, 3, 5, 7, 11]"
            :key="val"
            size="sm"
            :variant="modelValue.votes === val ? 'outline-primary' : 'outline-light'"
            :active="modelValue.votes === val"
            @click="updateVotes(val)"
          >
            {{ val === 1 ? 'All' : `&ge; ${val}` }}
          </BButton>
        </BButtonGroup>
      </BCard>
    </div>

    <!-- IP Family Filter -->
    <div class="col-md-5 col-12">
      <BCard class="h-100 mb-0" body-class="p-3">
        <span
          class="d-block small text-uppercase text-muted mb-2 ls-1"
          style="letter-spacing: 1px; font-size: 0.75rem"
        >
          IP Family
        </span>
        <BButtonGroup class="w-100">
          <BButton
            size="sm"
            variant="outline-light"
            :active="modelValue.family === 'all'"
            @click="updateFamily('all')"
            >All</BButton
          >
          <BButton
            size="sm"
            variant="outline-light"
            :active="modelValue.family === 'v4'"
            @click="updateFamily('v4')"
            >IPv4</BButton
          >
          <BButton
            size="sm"
            variant="outline-light"
            :active="modelValue.family === 'v6'"
            @click="updateFamily('v6')"
            >IPv6</BButton
          >
        </BButtonGroup>
      </BCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { FilterState } from '../types'
import { BCard, BButtonGroup, BButton } from 'bootstrap-vue-next'

const props = defineProps<{ modelValue: FilterState }>()
const emit = defineEmits<{ 'update:modelValue': [value: FilterState] }>()

const updateVotes = (v: number) => emit('update:modelValue', { ...props.modelValue, votes: v })
const updateFamily = (f: 'all' | 'v4' | 'v6') =>
  emit('update:modelValue', { ...props.modelValue, family: f })
</script>
