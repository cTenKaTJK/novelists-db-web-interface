<template>
  <div class="card">
    <div class="card-title">➕ Добавить произведение</div>
    <form @submit.prevent="submit">
      <div class="form-group">
        <input v-model="название" placeholder="Название произведения" required />
      </div>
      <div class="form-group">
        <select v-model="автор_id" required>
          <option disabled value="">-- Выберите автора --</option>
          <option v-for="w in props.writers" :key="w.id_писателя" :value="w.id_писателя">
            {{ w.фамилия }} {{ w.имя }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <select v-model="жанр_id" required>
          <option disabled value="">-- Выберите жанр --</option>
          <option v-for="g in props.genres" :key="g.id_жанра" :value="g.id_жанра">
            {{ g.жанр }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <input type="number" v-model.number="год_написания" placeholder="Год написания (необязательно)" />
      </div>
      <button type="submit" class="btn" :disabled="loading">Добавить</button>
      <div v-if="message" class="message">{{ message }}</div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { createWork } from '@/api/works'
import type { Writer, Genre } from '@/types'

const props = defineProps<{ writers: Writer[]; genres: Genre[] }>()
const emit = defineEmits(['added'])

const название = ref('')
const автор_id = ref<number | null>(null)
const жанр_id = ref<number | null>(null)
const год_написания = ref<number | undefined>()
const loading = ref(false)
const message = ref('')

async function submit() {
  if (!название.value || !автор_id.value || !жанр_id.value) return
  loading.value = true
  try {
    await createWork({
      название_произведения: название.value,
      автор_id: автор_id.value,
      id_жанра: жанр_id.value,
      год_написания: год_написания.value || null
    })
    message.value = 'Произведение добавлено!'
    название.value = ''
    автор_id.value = null
    жанр_id.value = null
    год_написания.value = undefined
    emit('added')
    setTimeout(() => message.value = '', 2000)
  } catch (err) {
    console.error(err)
    message.value = 'Ошибка добавления'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.message { margin-top: 0.5rem; font-size: 0.875rem; }
</style>