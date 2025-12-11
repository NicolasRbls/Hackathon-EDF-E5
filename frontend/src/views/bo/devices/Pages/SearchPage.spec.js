import { mount } from '@vue/test-utils';
import { describe, it, expect, vi } from 'vitest';
import SearchPage from './SearchPage.vue';
import axios from 'axios';

vi.mock('axios');

describe('SearchPage', () => {
  it('renders correctly', () => {
    const wrapper = mount(SearchPage);
    expect(wrapper.find('h1').text()).toBe('Recherche Matériel');
  });

  it('performs search on button click', async () => {
    const wrapper = mount(SearchPage);
    axios.get.mockResolvedValue({ data: [] });
    await wrapper.find('button').trigger('click');
    expect(axios.get).toHaveBeenCalled();
  });
});