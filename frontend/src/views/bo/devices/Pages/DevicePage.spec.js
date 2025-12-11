import { mount } from '@vue/test-utils';
import { describe, it, expect, vi } from 'vitest';
import DevicePage from './DevicePage.vue';
import axios from 'axios';
import { useRoute } from 'vue-router';

vi.mock('axios');
vi.mock('vue-router', () => ({
  useRoute: vi.fn(),
  useRouter: vi.fn(() => ({ push: vi.fn() }))
}));

describe('DevicePage', () => {
  it('loads device details', async () => {
    const { useRoute } = await import('vue-router');
    useRoute.mockReturnValue({ params: { serial: '123' } });
    axios.get.mockResolvedValue({ data: { serial_number: '123' } });
    const wrapper = mount(DevicePage);
    expect(axios.get).toHaveBeenCalled();
  });
});