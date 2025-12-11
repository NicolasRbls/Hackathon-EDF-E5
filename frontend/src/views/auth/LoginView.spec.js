import { mount } from '@vue/test-utils';
import { describe, it, expect, vi } from 'vitest';
import LoginView from './LoginView.vue';
import { authService } from '../../services/api';
import { useRouter } from 'vue-router';

// Mock dependencies
vi.mock('vue-router', () => ({
  useRouter: vi.fn(() => ({
    push: vi.fn()
  }))
}));

vi.mock('../../services/api', () => ({
  authService: {
    login: vi.fn(),
    getUserRole: vi.fn()
  }
}));

describe('LoginView', () => {
    it('renders login form', () => {
        const wrapper = mount(LoginView);
        expect(wrapper.find('h2').text()).toBe('Connexion');
        expect(wrapper.find('input[type=''text'']').exists()).toBe(true);
        expect(wrapper.find('input[type=''password'']').exists()).toBe(true);
    });

    it('calls login on submit', async () => {
        const wrapper = mount(LoginView);
        const pushMock = useRouter().push;
        
        // Fill form
        await wrapper.find('input[type=''text'']').setValue('admin');
        await wrapper.find('input[type=''password'']').setValue('password');
        
        // Mock success
        authService.login.mockResolvedValue({ token: 'fake-token' });
        authService.getUserRole.mockReturnValue('admin');

        await wrapper.find('form').trigger('submit.prevent');

        expect(authService.login).toHaveBeenCalledWith('admin', 'password');
        // Flush promises
        await new Promise(resolve => setTimeout(resolve, 0));
        expect(pushMock).toHaveBeenCalledWith('/admin');
    });

    it('shows error on failure', async () => {
        const wrapper = mount(LoginView);
        
        authService.login.mockRejectedValue({ response: { status: 401 } });
        
        await wrapper.find('input[type=''text'']').setValue('bad');
        await wrapper.find('input[type=''password'']').setValue('guy');
        await wrapper.find('form').trigger('submit.prevent');

        await new Promise(resolve => setTimeout(resolve, 0));
        
        expect(wrapper.text()).toContain('Identifiant ou mot de passe incorrect');
    });
});