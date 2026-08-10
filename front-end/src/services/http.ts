import axios, { AxiosError } from 'axios'

export class ApiError extends Error {
  readonly status: number | null

  constructor(message: string, status: number | null) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

export const httpClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 15_000,
})

httpClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<{ detail?: string }>) => {
    if (error.response) {
      const detail = error.response.data?.detail
      const message =
        detail ??
        (error.response.status === 503
          ? 'The SpaceX API is temporarily unavailable. Please try again shortly.'
          : `Request failed with status ${error.response.status}.`)
      return Promise.reject(new ApiError(message, error.response.status))
    }
    if (error.request) {
      return Promise.reject(
        new ApiError('Could not reach the API. Check your connection and that the backend is running.', null),
      )
    }
    return Promise.reject(new ApiError(error.message, null))
  },
)
