<template>
  <form @submit.prevent="onSubmit">
    <div class="form-group">
      <input v-model="local.фамилия" placeholder="Фамилия" required />
    </div>
    <div class="form-group">
      <input v-model="local.имя" placeholder="Имя" required />
    </div>
    <div class="form-group">
      <input v-model="local.отчество" placeholder="Отчество" />
    </div>
    <div class="form-group">
      <input type="number" v-model="local.год_рождения" placeholder="Год рождения" />
    </div>
    <div class="form-group">
      <input type="number" v-model="local.год_смерти" placeholder="Год смерти" />
    </div>

    <div class="form-group">
      <select v-model="local.id_страны_рождения">
        <option value="">-- Выберите страну --</option>
        <option v-for="c in props.countries" :key="c.id_страны" :value="c.id_страны">
          {{ c.название_страны }}
        </option>
      </select>
    </div>

    <button type="submit" class="btn">{{ isEdit ? 'Обновить' : 'Добавить' }}</button>
  </form>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
import type { Writer } from '@/types'

const props = defineProps<{
  initial?: Writer | null
  countries: { id_страны: number; название_страны: string }[]
}>()

const emit = defineEmits<{ (e: 'submit', data: Omit<Writer, 'id_писателя'>): void }>()

const local = reactive({
  фамилия: '',
  имя: '',
  отчество: '',
  год_рождения: '',
  год_смерти: '',
  id_страны_рождения: ''
})

const isEdit = !!props.initial

watch(() => props.initial, (newVal) => {
  if (newVal) {
    local.фамилия = newVal.фамилия
    local.имя = newVal.имя
    local.отчество = newVal.отчество || ''
    local.год_рождения = newVal.год_рождения?.toString() || ''
    local.год_смерти = newVal.год_смерти?.toString() || ''
    local.id_страны_рождения = newVal.id_страны_рождения?.toString() || ''
  } else {
    // Очистка при создании нового
    local.фамилия = ''
    local.имя = ''
    local.отчество = ''
    local.год_рождения = ''
    local.год_смерти = ''
    local.id_страны_рождения = ''
  }
}, { immediate: true })

function onSubmit() {
  const data: Omit<Writer, 'id_писателя'> = {
    фамилия: local.фамилия,
    имя: local.имя,
    отчество: local.отчество || null,
    год_рождения: local.год_рождения === '' ? null : Number(local.год_рождения),
    год_смерти: local.год_смерти === '' ? null : Number(local.год_смерти),
    id_страны_рождения: local.id_страны_рождения === '' ? null : Number(local.id_страны_рождения)
  }
  emit('submit', data)
}
</script>