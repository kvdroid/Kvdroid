from kvdroid import require_api
from kvdroid.jclass.android import VibrationEffect as VibrationEffectJava


@require_api(">=", 26)
class VibrationEffect:
    __slots__ = ("effect",)

    def __init__(self):
        self.effect = None

    @staticmethod
    def __get_self():
        return VibrationEffect

    __self = __get_self

    def create_one_shot(self, milliseconds: int, amplitude: int):
        self.effect = VibrationEffectJava().createOneShot(milliseconds, amplitude)

    @require_api(">=", 29)
    def create_predefined(self, effect_id: int):
        self.effect = VibrationEffectJava().createPredefined(effect_id)

    @require_api(">=", 36)
    def create_repeating_effect(
        self,
        preamble: __self() = None,
        repeating_effect: __self() = None,
        effect: __self() = None,
    ):
        if preamble is not None and repeating_effect is not None:
            self.effect = VibrationEffectJava().createRepeating(
                preamble, repeating_effect
            )
        elif effect is not None:
            self.effect = VibrationEffectJava().createRepeating(effect)
        else:
            raise ValueError("Invalid arguments")

    def create_waveform(
        self,
        timings: list[int],
        repeat: int,
        amplitudes: list[int] = None,
    ):
        if amplitudes is None:
            self.effect = VibrationEffectJava().createWaveform(timings, repeat, timings)
        else:
            self.effect = VibrationEffectJava().createWaveform(
                timings, amplitudes, repeat
            )

    def get_effect(self):
        return self.effect
