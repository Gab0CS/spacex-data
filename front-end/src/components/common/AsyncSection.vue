<script setup lang="ts">
import LoadingState from './LoadingState.vue'
import ErrorState from './ErrorState.vue'

withDefaults(
  defineProps<{
    isLoading: boolean
    error?: string | null
    loadingLabel?: string
  }>(),
  { error: null, loadingLabel: undefined },
)

const emit = defineEmits<{ retry: [] }>()
</script>

<template>
  <LoadingState v-if="isLoading" :label="loadingLabel" />
  <ErrorState v-else-if="error" :message="error" @retry="emit('retry')" />
  <slot v-else />
</template>
