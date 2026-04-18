<template>
  <div class="login-container">
    <div class="login-box">

      <h1 class="login-title">Daftar Akun<br/>Baru</h1>
      <p class="login-subtitle">Buat akun untuk mulai belajar</p>

      <div class="login-form">

        <input
          v-model="form.username"
          type="text"
          placeholder="username"
          class="input-field"
          @keyup.enter="handleRegister"
        />

        <input
          v-model="form.password"
          type="password"
          placeholder="password"
          class="input-field"
          @keyup.enter="handleRegister"
        />

        <input
          v-model="form.confirmPassword"
          type="password"
          placeholder="konfirmasi password"
          class="input-field"
          @keyup.enter="handleRegister"
        />

        <p v-if="errorMsg" class="error-message">{{ errorMsg }}</p>
        <p v-if="successMsg" class="success-message">{{ successMsg }}</p>

        <button
          class="btn-primary"
          :disabled="authStore.loading"
          @click="handleRegister"
        >
          <span v-if="authStore.loading">Mendaftar...</span>
          <span v-else>sign in</span>
        </button>

        <p class="register-link" @click="goToLogin">log in</p>

      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  username: '',
  password: '',
  confirmPassword: '',
})

const errorMsg = ref('')
const successMsg = ref('')

async function handleRegister() {
  errorMsg.value = ''
  successMsg.value = ''

  if (!form.username || !form.password || !form.confirmPassword) {
    errorMsg.value = 'Semua kolom harus diisi'
    return
  }

  if (form.password !== form.confirmPassword) {
    errorMsg.value = 'Password tidak cocok'
    return
  }

  const success = await authStore.register(form.username, form.password)

  if (success) {
    successMsg.value = 'Akun berhasil dibuat! Mengarahkan ke login...'
    setTimeout(() => router.push({ name: 'Login' }), 1500)
  } else {
    errorMsg.value = authStore.error || 'Registrasi gagal'
  }
}

function goToLogin() {
  router.push({ name: 'Login' })
}
</script>

<style scoped>
.login-container {
  width: 100vw;
  height: 100vh;
  background-color: var(--bg-primary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 480px;
  padding: 0 32px;
  gap: 12px;
}

.login-title {
  font-size: 28px;
  font-weight: 700;
  text-align: center;
  color: var(--text-primary);
  line-height: 1.3;
  margin-bottom: 4px;
}

.login-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  text-align: center;
  margin-bottom: 16px;
}

.login-form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.input-field {
  width: 100%;
  padding: 16px 20px;
  background-color: var(--bg-primary);
  border: 2px solid var(--accent);
  border-radius: var(--border-radius-lg);
  color: var(--text-primary);
  font-size: 16px;
  transition: var(--transition);
}

.input-field::placeholder {
  color: var(--text-secondary);
  opacity: 0.8;
}

.input-field:focus {
  outline: none;
  border-color: var(--accent-hover);
  box-shadow: 0 0 0 3px var(--accent-light);
}

.btn-primary {
  width: 100%;
  padding: 16px;
  background-color: var(--accent);
  color: var(--text-primary);
  border: none;
  border-radius: var(--border-radius-lg);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
  margin-top: 4px;
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--accent-hover);
  transform: translateY(-1px);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  color: #7b0000;
  background-color: #ffcccc55;
  padding: 8px 14px;
  border-radius: var(--border-radius-sm);
  font-size: 14px;
  text-align: center;
}

.success-message {
  color: #003300;
  background-color: #ccffcc55;
  padding: 8px 14px;
  border-radius: var(--border-radius-sm);
  font-size: 14px;
  text-align: center;
}

.register-link {
  text-align: center;
  font-size: 15px;
  color: var(--text-primary);
  cursor: pointer;
  margin-top: 4px;
}

.register-link:hover {
  text-decoration: underline;
}
</style>