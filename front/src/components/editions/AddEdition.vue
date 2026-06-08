<template>
  <div class="card">
    <div class="card-title">➕ Добавить издание</div>
    <form @submit.prevent="submit">
      <div class="form-group">
        <select v-model="id_произведения" required>
          <option disabled value="">-- Выберите произведение --</option>
          <option v-for="w in props.works" :key="w.id_произведения" :value="w.id_произведения">
            {{ w.название_произведения }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <select v-model="страна_где_издавалось" required>
          <option disabled value="">-- Выберите страну --</option>
          <option v-for="c in props.countries" :key="c.id_страны" :value="c.id_страны">
            {{ c.название_страны }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <input type="number" v-model.number="год_издания" placeholder="Год издания" required />
      </div>
      <div class="form-group">
        <input type="number" v-model.number="тираж_издания" placeholder="Тираж" required />
      </div>
      <div class="form-group">
        <input v-model="издательство" placeholder="Издательство (необязательно)" />
      </div>
      <button type="submit" class="btn" :disabled="loading">Добавить</button>
      <div v-if="message" class="message">{{ message }}</div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { createEdition } from '@/api/editions'

const props = defineProps<{
  works: { id_произведения: number; название_произведения: string }[]
  countries: { id_страны: number; название_страны: string }[]
}>()
const emit = defineEmits(['added'])

const id_произведения = ref<number | null>(null)
const страна_где_издавалось = ref<number | null>(null)
const год_издания = ref<number | undefined>()
const тираж_издания = ref<number | undefined>()
const издательство = ref('')
const loading = ref(false)
const message = ref('')

async function submit() {
  if (!id_произведения.value || !страна_где_издавалось.value || !год_издания.value || !тираж_издания.value) return
  loading.value = true
  try {
    await createEdition({
      id_произведения: id_произведения.value,
      страна_где_издавалось: страна_где_издавалось.value,
      год_издания: год_издания.value,
      тираж_издания: тираж_издания.value,
      издательство: издательство.value || null
    })
    message.value = '✅ Издание добавлено!'
    // очистка
    id_произведения.value = null
    страна_где_издавалось.value = null
    год_издания.value = undefined
    тираж_издания.value = undefined
    издательство.value = ''
    emit('added')
    setTimeout(() => message.value = '', 3000)
  } catch (err) {
    console.error(err)
    message.value = '❌ Ошибка добавления издания'
  } finally {
    loading.value = false
  }
}
</script>