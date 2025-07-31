// Fichier de suppression temporaire des erreurs TypeScript pour React 19
// Ces déclarations corrigent les erreurs d'import des hooks React et composants React Native
// jusqu'à ce que les types officiels soient mis à jour

declare module 'react' {
  export function useState<T>(initialState: T | (() => T)): [T, (value: T | ((prev: T) => T)) => void];
  export function useEffect(effect: () => void | (() => void), deps?: any[]): void;
  export function useLayoutEffect(effect: () => void | (() => void), deps?: any[]): void;
  export function useRef<T>(initialValue: T): { current: T };
  export function useCallback<T extends (...args: any[]) => any>(callback: T, deps: any[]): T;
  export function useMemo<T>(factory: () => T, deps: any[]): T;
  export function useContext<T>(context: any): T;
  export function useReducer<T, A>(reducer: (state: T, action: A) => T, initialState: T): [T, (action: A) => void];
}

declare module 'react-native' {
  export const View: any;
  export const Text: any;
  export const TouchableOpacity: any;
  export const StyleSheet: any;
  export const Alert: any;
  export const Dimensions: any;
  export const Animated: any;
  export const ScrollView: any;
  export const Image: any;
  export const TextInput: any;
  export const SafeAreaView: any;
  export const StatusBar: any;
  export const Platform: any;
  export const Linking: any;
}
