import { mount } from '@vue/test-utils';
import { describe, it, expect, vi } from 'vitest';
import ScanPage from './ScanPage.vue';
import axios from 'axios';
import { BrowserMultiFormatReader } from '@zxing/library';

vi.mock('axios');
vi.mock('@zxing/library', () => {
  return {
    BrowserMultiFormatReader: vi.fn(() => ({
      listVideoInputDevices: vi.fn(),
      decodeFromVideoDevice: vi.fn(),
      reset: vi.fn()
    })),
    NotFoundException: class {}
  };
});

describe('ScanPage', () => {
  it('renders correctly', () => {
    const wrapper = mount(ScanPage);
    expect(wrapper.find('h1').text()).toBe('Scanner un Appareil');
  });
});