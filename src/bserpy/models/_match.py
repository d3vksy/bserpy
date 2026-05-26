from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class BattleUserResult:  # noqa: PLR0902
    """매치 내 플레이어 한 명의 결과 데이터.

    실측 기반 315개 필드 정의.
    API 업데이트로 추가된 필드는 Optional로 처리하여 내성을 확보.
    """

    # ── 기본 식별 ────────────────────────────────────────
    nickname: str
    game_id: int
    season_id: int
    matching_mode: int
    matching_team_mode: int

    # ── 캐릭터/스킨 ──────────────────────────────────────
    character_num: int
    skin_code: int
    character_level: int

    # ── 경기 결과 ────────────────────────────────────────
    game_rank: int
    victory: int
    player_kill: int
    player_assistant: int
    monster_kill: int
    player_deaths: int

    # ── 무기/장비 ────────────────────────────────────────
    best_weapon: int
    best_weapon_level: int
    mastery_level: dict[str, int]
    equipment: dict[str, int]
    equipment_grade: dict[str, int]          # 문서 미기재, 실제 존재

    # ── 버전 ─────────────────────────────────────────────
    version_season: int | None
    version_major: int
    version_minor: int
    language: str

    # ── 스킬 ─────────────────────────────────────────────
    skill_level_info: dict[str, int]
    skill_order_info: dict[str, int]

    # ── 서버/시간 ────────────────────────────────────────
    server_name: str
    start_dtm: str
    duration: int
    play_time: int
    watch_time: int
    total_time: int
    expire_dtm: str | None = None            # 문서 미기재, 실제 존재
    survivable_time: int | None = None       # 문서 미기재, 실제 존재

    # ── MMR ──────────────────────────────────────────────
    mmr_before: int | None = None
    mmr_gain: int | None = None
    mmr_after: int | None = None
    mmr_avg: int | None = None
    rank_point: int | None = None            # 문서 미기재, 실제 존재 (mmrAfter 와 동일값)
    mmr_gain_in_game: int | None = None
    mmr_loss_entry_cost: int | None = None

    # ── 스탯 ─────────────────────────────────────────────
    max_hp: int = 0
    max_sp: int = 0
    attack_power: int = 0
    defense: int = 0
    hp_regen: float = 0.0
    sp_regen: float = 0.0
    attack_speed: float = 0.0
    move_speed: float = 0.0
    out_of_combat_move_speed: float = 0.0
    sight_range: float = 0.0
    attack_range: float = 0.0
    critical_strike_chance: float = 0.0
    critical_strike_damage: float = 0.0
    cool_down_reduction: float = 0.0
    life_steal: float = 0.0
    normal_life_steal: float = 0.0
    skill_life_steal: float = 0.0
    amplifier_to_monster: float = 0.0
    trap_damage: float = 0.0
    adaptive_force: int = 0
    adaptive_force_attack: int = 0
    adaptive_force_amplify: int = 0
    skill_amp: int = 0

    # ── 경험치/크레딧 ────────────────────────────────────
    gain_exp: int = 0
    base_exp: int | None = None              # 문서 미기재
    bonus_exp: int | None = None             # 문서 미기재
    bonus_coin: int | None = None            # 문서 미기재

    # ── 피해량 (대 플레이어) ─────────────────────────────
    damage_to_player: int = 0
    damage_to_player_trap: int = 0
    damage_to_player_basic: int = 0
    damage_to_player_skill: int = 0
    damage_to_player_item_skill: int = 0
    damage_to_player_direct: int = 0
    damage_to_player_unique_skill: int = 0
    damage_to_player_shield: int = 0

    # ── 피해량 (받음, 플레이어) ──────────────────────────
    damage_from_player: int = 0
    damage_from_player_trap: int = 0
    damage_from_player_basic: int = 0
    damage_from_player_skill: int = 0
    damage_from_player_item_skill: int = 0
    damage_from_player_direct: int = 0
    damage_from_player_unique_skill: int = 0

    # ── 피해량 (대 몬스터) ───────────────────────────────
    damage_to_monster: int = 0
    damage_to_monster_trap: int = 0
    damage_to_monster_basic: int = 0
    damage_to_monster_skill: int = 0
    damage_to_monster_item_skill: int = 0
    damage_to_monster_direct: int = 0
    damage_to_monster_unique_skill: int = 0
    damage_from_monster: int = 0

    # ── 보호막 ───────────────────────────────────────────
    damage_offseted_by_shield_player: int = 0
    damage_offseted_by_shield_monster: int = 0
    protect_absorb: int = 0

    # ── 몬스터 처치 ──────────────────────────────────────
    kill_monsters: dict[str, int] = field(default_factory=dict)

    # ── 회복/지원 ────────────────────────────────────────
    heal_amount: int = 0
    team_recover: int = 0

    # ── 카메라/시설 ──────────────────────────────────────
    add_surveillance_camera: int = 0
    add_telephoto_camera: int = 0
    remove_surveillance_camera: int = 0
    remove_telephoto_camera: int = 0
    use_hyper_loop: int = 0
    use_security_console: int = 0

    # ── 팀/매칭 ──────────────────────────────────────────
    bot_added: int = 0
    bot_remain: int = 0
    restricted_area_accelerated: int = 0
    safe_areas: int = 0
    team_number: int = 0
    pre_made: int = 0
    match_size: int | None = None            # 문서 미기재, 실제 존재
    team_kill: int = 0
    total_field_kill: int | None = None      # 문서 미기재, 실제 존재
    premade_matching_type: int | None = None

    # ── 경로/위치 ────────────────────────────────────────
    route_id_of_start: int = 0
    route_slot_id: int = 0
    place_of_start: str = ""

    # ── 계정 ─────────────────────────────────────────────
    account_level: int = 0

    # ── 사망 정보 (레거시, 해석 미지원) ──────────────────
    killer: str | None = None
    kill_detail: str | None = None
    cause_of_death: str | None = None
    place_of_death: str | None = None
    killer_character: str | None = None
    killer_weapon: str | None = None
    killer2: str | None = None
    kill_detail2: str | None = None
    cause_of_death2: str | None = None
    place_of_death2: str | None = None
    killer_character2: str | None = None
    killer_weapon2: str | None = None
    killer3: str | None = None
    kill_detail3: str | None = None
    cause_of_death3: str | None = None
    place_of_death3: str | None = None
    killer_character3: str | None = None
    killer_weapon3: str | None = None

    # ── 기타 액션 ────────────────────────────────────────
    give_up: int = 0
    team_spectator: int = 0
    gained_normal_mmr_k_factor: float = 0.0
    fishing_count: int = 0
    use_emoticon_count: int = 0
    escape_state: int | None = None

    # ── 제작 ─────────────────────────────────────────────
    craft_uncommon: int = 0
    craft_rare: int = 0
    craft_epic: int = 0
    craft_legend: int = 0
    craft_mythic: int = 0
    camp_fire_craft_uncommon: int = 0
    camp_fire_craft_rare: int = 0
    camp_fire_craft_epic: int = 0
    camp_fire_craft_legendary: int = 0

    # ── 특성 ─────────────────────────────────────────────
    trait_first_core: int = 0
    trait_first_sub: list[int] = field(default_factory=list)
    trait_second_sub: list[int] = field(default_factory=list)

    # ── VF 크레딧 ────────────────────────────────────────
    total_vf_credits: list[int] = field(default_factory=list)   # 실제: totalVFCredits (배열)
    used_vf_credits: list[int] = field(default_factory=list)    # 실제: usedVFCredits (배열)
    actively_gained_credits: int | None = None                   # 문서 미기재
    sum_used_vf_credits: int | None = None                       # 문서 미기재
    total_gain_vf_credit: int = 0
    total_use_vf_credit: int = 0

    # ── VF 크레딧 획득 출처 ──────────────────────────────
    kill_player_gain_vf_credit: int = 0
    kill_chicken_gain_vf_credit: int = 0
    kill_boar_gain_vf_credit: int = 0
    kill_wild_dog_gain_vf_credit: int = 0
    kill_wolf_gain_vf_credit: int = 0
    kill_bear_gain_vf_credit: int = 0
    kill_omega_gain_vf_credit: int = 0
    kill_bat_gain_vf_credit: int = 0
    kill_wickline_gain_vf_credit: int = 0
    kill_alpha_gain_vf_credit: int = 0
    kill_item_bounty_gain_vf_credit: int = 0
    kill_drone_gain_vf_credit: int = 0
    kill_gamma_gain_vf_credit: int = 0
    kill_turret_gain_vf_credit: int = 0
    item_shredder_gain_vf_credit: int = 0

    # ── VF 크레딧 사용처 ─────────────────────────────────
    remote_drone_use_vf_credit_my_self: int = 0
    remote_drone_use_vf_credit_ally: int = 0
    kiosk_from_material_use_vf_credit: int = 0      # 실제: kioskFromMaterialUseVFCredit
    kiosk_from_escape_key_use_vf_credit: int = 0    # 실제: kioskFromEscapeKeyUseVFCredit
    kiosk_from_revival_use_vf_credit: int = 0       # 실제: kioskFromRevivalUseVFCredit
    tactical_skill_upgrade_use_vf_credit: int = 0

    # ── cr 크레딧 계열 ───────────────────────────────────
    cr_get_animal: int = 0
    cr_get_mutant: int = 0
    cr_get_phase_start: int = 0
    cr_get_kill: int = 0
    cr_get_assist: int = 0
    cr_get_time_elapsed: int = 0
    cr_get_credit_bonus: int = 0
    cr_use_remote_drone: int = 0
    cr_use_upgrade_tactical_skill: int = 0
    cr_use_tree_of_life: int = 0
    cr_use_meteorite: int | None = None              # 문서 미기재, 실제 존재
    cr_use_mythril: int = 0
    cr_use_force_core: int = 0
    cr_use_vf_blood_sample: int = 0
    cr_use_activation_module: int | None = None      # 문서 미기재
    cr_use_rootkit: int = 0
    kiosk_exchange_credit: int = 0

    # ── 팀 전투 집계 ─────────────────────────────────────
    team_elimination: int = 0
    team_down: int = 0
    team_battle_zone_down: int = 0
    team_repeat_down: int = 0
    team_down_can_not_eliminate: int | None = None   # 문서 미기재
    team_down_can_eliminate: int | None = None       # 문서 미기재
    team_repeat_down_can_not_eliminate: int | None = None
    team_repeat_down_can_eliminate: int | None = None
    terminate_count: int = 0
    terminate_count_can_not_eliminate: int | None = None
    break_count: int | None = None                   # 문서 미기재
    clutch_count: int = 0
    unknown_kill: int = 0

    # ── 멀티킬 ───────────────────────────────────────────
    total_double_kill: int = 0
    total_triple_kill: int = 0
    total_quadra_kill: int = 0
    total_extra_kill: int = 0
    kill_gamma: bool | None = None

    # ── 전술 스킬 ────────────────────────────────────────
    tactical_skill_group: int = 0
    tactical_skill_level: int = 0
    tactical_skill_use_count: int = 0

    # ── 부활/이탈 ────────────────────────────────────────
    credit_revival_count: int = 0
    credit_revived_others_count: int = 0
    time_spent_in_briefing_room: int = 0
    is_leaving_before_credit_revival_terminate: bool | None = None
    innocente_give_up: bool | None = None

    # ── 드론/카메라 ──────────────────────────────────────
    view_contribution: int = 0
    use_recon_drone: int = 0
    use_emp_drone: int = 0
    except_pre_made_team: int = 0
    item_transferred_console: list[int] = field(default_factory=list)
    item_transferred_drone: list[int] = field(default_factory=list)

    # ── 날씨/환경 ────────────────────────────────────────
    main_weather: int = 0
    sub_weather: int = 0
    active_installation: dict[str, Any] = field(default_factory=dict)

    # ── 루미(가이드 로봇) ────────────────────────────────
    use_guide_robot: int = 0
    guide_robot_radial: int = 0
    guide_robot_flag_ship: int = 0
    guide_robot_signature: int = 0
    cr_get_by_guide_robot: int = 0
    damage_to_guide_robot: int = 0

    # ── 큐브 ─────────────────────────────────────────────
    get_buff_cube_red: int = 0
    get_buff_cube_purple: int = 0
    get_buff_cube_green: int = 0
    get_buff_cube_gold: int = 0
    get_buff_cube_sky_blue: int = 0
    sum_get_buff_cube: int = 0

    # ── 균열/난류 ────────────────────────────────────────
    enter_dimension_rift: int = 0
    enter_dimension_empowered_rift: int = 0
    win_from_dimension_rift: int = 0
    win_from_dimension_empowered_rift: int = 0
    enter_turbulent_rift: int = 0

    # ── 기믹 ─────────────────────────────────────────────
    gimmick_apple_dropped: int = 0
    gimmick_drum_use_count: int = 0
    gimmick_drum_attack_count: int = 0
    gimmick_drum_dropped_hit_count: int = 0
    gimmick_evidence_locker_count: Any | None = None
    gimmick_evidence_locker_item: list[int] = field(default_factory=list)
    gimmick_hospital_discount_rate: int = 0
    gimmick_grandfather_clock_use_count: int = 0

    # ── 기타 집계 ────────────────────────────────────────
    squad_rumble_rank: int | None = None
    total_turbine_take_over: int | None = None
    total_tk_per_min: float | None = None
    resurrection_kit_usage_count: int | None = None
    resurrection_kit_to_credit: int | None = None
    using_default_game_option: bool | None = None
    reunited_count: int | None = None
    is_ml_bot: bool | None = None
    bot_level: int | None = None
    afk_dtm: str | None = None
    giveup_dtm: str | None = None
    milli_tournament_kill_score: int | None = None
    tournament_rank_score: int | None = None
    tree_of_life_spawn: list[int] = field(default_factory=list)

    # ── COBALT 전용 ──────────────────────────────────────
    starting_items: list[int] = field(default_factory=list)
    used_normal_heal_pack: int = 0
    used_reinforced_heal_pack: int = 0
    used_normal_shield_pack: int = 0      # 문서 오타: usedNormalShiedPack
    used_reinforce_shield_pack: int = 0   # 문서: usedReinforcedShieldPack
    bought_infusion: dict[str, Any] = field(default_factory=dict)
    final_infusion: list[int] = field(default_factory=list)
    scored_point: list[int] = field(default_factory=list)
    kills_phase_one: int | None = None
    kills_phase_two: int | None = None
    kills_phase_three: int | None = None
    deaths_phase_one: int | None = None
    deaths_phase_two: int | None = None
    deaths_phase_three: int | None = None
    infusion_re_roll_use_vf_credit: int = 0
    infusion_trait_use_vf_credit: int = 0
    infusion_relic_use_vf_credit: int = 0
    infusion_store_use_vf_credit: int = 0
    cobalt_random_pick_remove_character: int | None = None

    # ── deprecated 배틀존 ────────────────────────────────
    battle_zone1_area_code: int | None = None
    battle_zone1_battle_mark: int | None = None
    battle_zone2_area_code: int | None = None
    battle_zone2_battle_mark: int | None = None
    battle_zone3_area_code: int | None = None
    battle_zone3_battle_mark: int | None = None
    battle_zone1_winner: int | None = None
    battle_zone2_winner: int | None = None
    battle_zone3_winner: int | None = None
    battle_zone1_battle_mark_count: int | None = None
    battle_zone2_battle_mark_count: int | None = None
    battle_zone3_battle_mark_count: int | None = None

    # ── 복합 딕셔너리 필드 ───────────────────────────────
    event_mission_result: dict[str, Any] = field(default_factory=dict)
    kill_details: dict[str, Any] = field(default_factory=dict)
    death_details: dict[str, Any] = field(default_factory=dict)
    credit_source: dict[str, Any] = field(default_factory=dict)
    food_craft_count: list[int] = field(default_factory=list)
    beverage_craft_count: dict[str, Any] = field(default_factory=dict)
    air_supply_open_count: dict[str, Any] = field(default_factory=dict)
    collect_item_for_log: list[int] = field(default_factory=list)
    equip_first_item_for_log: dict[str, Any] = field(default_factory=dict)
    use_gadget: dict[str, Any] = field(default_factory=dict)
    get_bori_reward: dict[str, Any] = field(default_factory=dict)
    cc_time_to_player: float = 0.0

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> BattleUserResult:  # noqa: PLR0912,PLR0915
        return cls(
            nickname=d.get("nickname", ""),
            game_id=d["gameId"],
            season_id=d.get("seasonId", 0),
            matching_mode=d.get("matchingMode", 0),
            matching_team_mode=d.get("matchingTeamMode", 0),
            character_num=d.get("characterNum", 0),
            skin_code=d.get("skinCode", 0),
            character_level=d.get("characterLevel", 0),
            game_rank=d.get("gameRank", 0),
            victory=d.get("victory", 0),
            player_kill=d.get("playerKill", 0),
            player_assistant=d.get("playerAssistant", 0),
            monster_kill=d.get("monsterKill", 0),
            player_deaths=d.get("playerDeaths", 0),
            best_weapon=d.get("bestWeapon", 0),
            best_weapon_level=d.get("bestWeaponLevel", 0),
            mastery_level=d.get("masteryLevel", {}),
            equipment=d.get("equipment", {}),
            equipment_grade=d.get("equipmentGrade", {}),
            version_season=d.get("versionSeason"),
            version_major=d.get("versionMajor", 0),
            version_minor=d.get("versionMinor", 0),
            language=d.get("language", ""),
            skill_level_info=d.get("skillLevelInfo", {}),
            skill_order_info=d.get("skillOrderInfo", {}),
            server_name=d.get("serverName", ""),
            start_dtm=d.get("startDtm", ""),
            duration=d.get("duration", 0),
            play_time=d.get("playTime", 0),
            watch_time=d.get("watchTime", 0),
            total_time=d.get("totalTime", 0),
            expire_dtm=d.get("expireDtm"),
            survivable_time=d.get("survivableTime"),
            mmr_before=d.get("mmrBefore"),
            mmr_gain=d.get("mmrGain"),
            mmr_after=d.get("mmrAfter"),
            mmr_avg=d.get("mmrAvg"),
            rank_point=d.get("rankPoint"),
            mmr_gain_in_game=d.get("mmrGainInGame"),
            mmr_loss_entry_cost=d.get("mmrLossEntryCost"),
            max_hp=d.get("maxHp", 0),
            max_sp=d.get("maxSp", 0),
            attack_power=d.get("attackPower", 0),
            defense=d.get("defense", 0),
            hp_regen=d.get("hpRegen", 0.0),
            sp_regen=d.get("spRegen", 0.0),
            attack_speed=d.get("attackSpeed", 0.0),
            move_speed=d.get("moveSpeed", 0.0),
            out_of_combat_move_speed=d.get("outOfCombatMoveSpeed", 0.0),
            sight_range=d.get("sightRange", 0.0),
            attack_range=d.get("attackRange", 0.0),
            critical_strike_chance=d.get("criticalStrikeChance", 0.0),
            critical_strike_damage=d.get("criticalStrikeDamage", 0.0),
            cool_down_reduction=d.get("coolDownReduction", 0.0),
            life_steal=d.get("lifeSteal", 0.0),
            normal_life_steal=d.get("normalLifeSteal", 0.0),
            skill_life_steal=d.get("skillLifeSteal", 0.0),
            amplifier_to_monster=d.get("amplifierToMonster", 0.0),
            trap_damage=d.get("trapDamage", 0.0),
            adaptive_force=d.get("adaptiveForce", 0),
            adaptive_force_attack=d.get("adaptiveForceAttack", 0),
            adaptive_force_amplify=d.get("adaptiveForceAmplify", 0),
            skill_amp=d.get("skillAmp", 0),
            gain_exp=d.get("gainExp", 0),
            base_exp=d.get("baseExp"),
            bonus_exp=d.get("bonusExp"),
            bonus_coin=d.get("bonusCoin"),
            damage_to_player=d.get("damageToPlayer", 0),
            damage_to_player_trap=d.get("damageToPlayer_trap", 0),
            damage_to_player_basic=d.get("damageToPlayer_basic", 0),
            damage_to_player_skill=d.get("damageToPlayer_skill", 0),
            damage_to_player_item_skill=d.get("damageToPlayer_itemSkill", 0),
            damage_to_player_direct=d.get("damageToPlayer_direct", 0),
            damage_to_player_unique_skill=d.get("damageToPlayer_uniqueSkill", 0),
            damage_to_player_shield=d.get("damageToPlayer_Shield", 0),
            damage_from_player=d.get("damageFromPlayer", 0),
            damage_from_player_trap=d.get("damageFromPlayer_trap", 0),
            damage_from_player_basic=d.get("damageFromPlayer_basic", 0),
            damage_from_player_skill=d.get("damageFromPlayer_skill", 0),
            damage_from_player_item_skill=d.get("damageFromPlayer_itemSkill", 0),
            damage_from_player_direct=d.get("damageFromPlayer_direct", 0),
            damage_from_player_unique_skill=d.get("damageFromPlayer_uniqueSkill", 0),
            damage_to_monster=d.get("damageToMonster", 0),
            damage_to_monster_trap=d.get("damageToMonster_trap", 0),
            damage_to_monster_basic=d.get("damageToMonster_basic", 0),
            damage_to_monster_skill=d.get("damageToMonster_skill", 0),
            damage_to_monster_item_skill=d.get("damageToMonster_itemSkill", 0),
            damage_to_monster_direct=d.get("damageToMonster_direct", 0),
            damage_to_monster_unique_skill=d.get("damageToMonster_uniqueSkill", 0),
            damage_from_monster=d.get("damageFromMonster", 0),
            damage_offseted_by_shield_player=d.get("damageOffsetedByShield_Player", 0),
            damage_offseted_by_shield_monster=d.get("damageOffsetedByShield_Monster", 0),
            protect_absorb=d.get("protectAbsorb", 0),
            kill_monsters=d.get("killMonsters", {}),
            heal_amount=d.get("healAmount", 0),
            team_recover=d.get("teamRecover", 0),
            add_surveillance_camera=d.get("addSurveillanceCamera", 0),
            add_telephoto_camera=d.get("addTelephotoCamera", 0),
            remove_surveillance_camera=d.get("removeSurveillanceCamera", 0),
            remove_telephoto_camera=d.get("removeTelephotoCamera", 0),
            use_hyper_loop=d.get("useHyperLoop", 0),
            use_security_console=d.get("useSecurityConsole", 0),
            bot_added=d.get("botAdded", 0),
            bot_remain=d.get("botRemain", 0),
            restricted_area_accelerated=d.get("restrictedAreaAccelerated", 0),
            safe_areas=d.get("safeAreas", 0),
            team_number=d.get("teamNumber", 0),
            pre_made=d.get("preMade", 0),
            match_size=d.get("matchSize"),
            team_kill=d.get("teamKill", 0),
            total_field_kill=d.get("totalFieldKill"),
            premade_matching_type=d.get("premadeMatchingType"),
            route_id_of_start=d.get("routeIdOfStart", 0),
            route_slot_id=d.get("routeSlotId", 0),
            place_of_start=str(d.get("placeOfStart", "")),
            account_level=d.get("accountLevel", 0),
            killer=d.get("killer"),
            kill_detail=d.get("killDetail"),
            cause_of_death=d.get("causeOfDeath"),
            place_of_death=d.get("placeOfDeath"),
            killer_character=d.get("killerCharacter"),
            killer_weapon=d.get("killerWeapon"),
            killer2=d.get("killer2"),
            kill_detail2=d.get("killDetail2"),
            cause_of_death2=d.get("causeOfDeath2"),
            place_of_death2=d.get("placeOfDeath2"),
            killer_character2=d.get("killerCharacter2"),
            killer_weapon2=d.get("killerWeapon2"),
            killer3=d.get("killer3"),
            kill_detail3=d.get("killDetail3"),
            cause_of_death3=d.get("causeOfDeath3"),
            place_of_death3=d.get("placeOfDeath3"),
            killer_character3=d.get("killerCharacter3"),
            killer_weapon3=d.get("killerWeapon3"),
            give_up=d.get("giveUp", 0),
            team_spectator=d.get("teamSpectator", 0),
            gained_normal_mmr_k_factor=d.get("gainedNormalMmrKFactor", 0.0),
            fishing_count=d.get("fishingCount", 0),
            use_emoticon_count=d.get("useEmoticonCount", 0),
            escape_state=d.get("escapeState"),
            craft_uncommon=d.get("craftUncommon", 0),
            craft_rare=d.get("craftRare", 0),
            craft_epic=d.get("craftEpic", 0),
            craft_legend=d.get("craftLegend", 0),
            craft_mythic=d.get("craftMythic", 0),
            camp_fire_craft_uncommon=d.get("campFireCraftUncommon", 0),
            camp_fire_craft_rare=d.get("campFireCraftRare", 0),
            camp_fire_craft_epic=d.get("campFireCraftEpic", 0),
            camp_fire_craft_legendary=d.get("campFireCraftLegendary", 0),
            trait_first_core=d.get("traitFirstCore", 0),
            trait_first_sub=d.get("traitFirstSub", []),
            trait_second_sub=d.get("traitSecondSub", []),
            total_vf_credits=d.get("totalVFCredits", d.get("totalVFCredit", [])),
            used_vf_credits=d.get("usedVFCredits", d.get("usedVFCredit", [])),
            actively_gained_credits=d.get("activelyGainedCredits"),
            sum_used_vf_credits=d.get("sumUsedVFCredits"),
            total_gain_vf_credit=d.get("totalGainVFCredit", 0),
            total_use_vf_credit=d.get("totalUseVFCredit", 0),
            kill_player_gain_vf_credit=d.get("killPlayerGainVFCredit", 0),
            kill_chicken_gain_vf_credit=d.get("killChickenGainVFCredit", 0),
            kill_boar_gain_vf_credit=d.get("killBoarGainVFCredit", 0),
            kill_wild_dog_gain_vf_credit=d.get("killWildDogGainVFCredit", 0),
            kill_wolf_gain_vf_credit=d.get("killWolfGainVFCredit", 0),
            kill_bear_gain_vf_credit=d.get("killBearGainVFCredit", 0),
            kill_omega_gain_vf_credit=d.get("killOmegaGainVFCredit", 0),
            kill_bat_gain_vf_credit=d.get("killBatGainVFCredit", 0),
            kill_wickline_gain_vf_credit=d.get("killWicklineGainVFCredit", 0),
            kill_alpha_gain_vf_credit=d.get("killAlphaGainVFCredit", 0),
            kill_item_bounty_gain_vf_credit=d.get("killItemBountyGainVFCredit", 0),
            kill_drone_gain_vf_credit=d.get("killDroneGainVFCredit", 0),
            kill_gamma_gain_vf_credit=d.get("killGammaGainVFCredit", 0),
            kill_turret_gain_vf_credit=d.get("killTurretGainVFCredit", 0),
            item_shredder_gain_vf_credit=d.get("itemShredderGainVFCredit", 0),
            remote_drone_use_vf_credit_my_self=d.get("remoteDroneUseVFCreditMySelf", 0),
            remote_drone_use_vf_credit_ally=d.get("remoteDroneUseVFCreditAlly", 0),
            kiosk_from_material_use_vf_credit=d.get(
                "kioskFromMaterialUseVFCredit",
                d.get("transferConsoleFromMaterialUseVFCredit", 0),
            ),
            kiosk_from_escape_key_use_vf_credit=d.get(
                "kioskFromEscapeKeyUseVFCredit",
                d.get("transferConsoleFromEscapeKeyUseVFCredit", 0),
            ),
            kiosk_from_revival_use_vf_credit=d.get(
                "kioskFromRevivalUseVFCredit",
                d.get("transferConsoleFromRevivalUseVFCredit", 0),
            ),
            tactical_skill_upgrade_use_vf_credit=d.get("tacticalSkillUpgradeUseVFCredit", 0),
            cr_get_animal=d.get("crGetAnimal", 0),
            cr_get_mutant=d.get("crGetMutant", 0),
            cr_get_phase_start=d.get("crGetPhaseStart", 0),
            cr_get_kill=d.get("crGetKill", 0),
            cr_get_assist=d.get("crGetAssist", 0),
            cr_get_time_elapsed=d.get("crGetTimeElapsed", 0),
            cr_get_credit_bonus=d.get("crGetCreditBonus", 0),
            cr_use_remote_drone=d.get("crUseRemoteDrone", 0),
            cr_use_upgrade_tactical_skill=d.get("crUseUpgradeTacticalSkill", 0),
            cr_use_tree_of_life=d.get("crUseTreeOfLife", 0),
            cr_use_meteorite=d.get("crUseMeteorite"),
            cr_use_mythril=d.get("crUseMythril", 0),
            cr_use_force_core=d.get("crUseForceCore", 0),
            cr_use_vf_blood_sample=d.get("crUseVFBloodSample", 0),
            cr_use_activation_module=d.get("crUseActivationModule"),
            cr_use_rootkit=d.get("crUseRootkit", 0),
            kiosk_exchange_credit=d.get("kioskExchangeCredit", 0),
            team_elimination=d.get("teamElimination", 0),
            team_down=d.get("teamDown", 0),
            team_battle_zone_down=d.get("teamBattleZoneDown", 0),
            team_repeat_down=d.get("teamRepeatDown", 0),
            team_down_can_not_eliminate=d.get("teamDownCanNotEliminate"),
            team_down_can_eliminate=d.get("teamDownCanEliminate"),
            team_repeat_down_can_not_eliminate=d.get("teamRepeatDownCanNotEliminate"),
            team_repeat_down_can_eliminate=d.get("teamRepeatDownCanEliminate"),
            terminate_count=d.get("terminateCount", 0),
            terminate_count_can_not_eliminate=d.get("terminateCountCanNotEliminate"),
            break_count=d.get("breakCount"),
            clutch_count=d.get("clutchCount", 0),
            unknown_kill=d.get("unknownKill", 0),
            total_double_kill=d.get("totalDoubleKill", 0),
            total_triple_kill=d.get("totalTripleKill", 0),
            total_quadra_kill=d.get("totalQuadraKill", 0),
            total_extra_kill=d.get("totalExtraKill", 0),
            kill_gamma=d.get("killGamma"),
            tactical_skill_group=d.get("tacticalSkillGroup", 0),
            tactical_skill_level=d.get("tacticalSkillLevel", 0),
            tactical_skill_use_count=d.get("tacticalSkillUseCount", 0),
            credit_revival_count=d.get("creditRevivalCount", 0),
            credit_revived_others_count=d.get("creditRevivedOthersCount", 0),
            time_spent_in_briefing_room=d.get("timeSpentInBriefingRoom", 0),
            is_leaving_before_credit_revival_terminate=(
                d.get("IsLeavingBeforeCreditRevivalTerminate")
                or d.get("isLeavingBeforeCreditRevivalTerminate")
            ),
            innocente_give_up=d.get("innocentGiveUp") or d.get("isInnocentGiveUp"),
            view_contribution=d.get("viewContribution", 0),
            use_recon_drone=d.get("useReconDrone", 0),
            use_emp_drone=d.get("useEmpDrone", 0),
            except_pre_made_team=d.get("exceptPreMadeTeam", 0),
            item_transferred_console=d.get("itemTransferredConsole", []),
            item_transferred_drone=d.get("itemTransferredDrone", []),
            main_weather=d.get("mainWeather", 0),
            sub_weather=d.get("subWeather", 0),
            active_installation=d.get("activeInstallation", {}),
            use_guide_robot=d.get("useGuideRobot", 0),
            guide_robot_radial=d.get("guideRobotRadial", 0),
            guide_robot_flag_ship=d.get("guideRobotFlagShip", 0),
            guide_robot_signature=d.get("guideRobotSignature", 0),
            cr_get_by_guide_robot=d.get("crGetByGuideRobot", 0),
            damage_to_guide_robot=d.get("damageToGuideRobot", 0),
            get_buff_cube_red=d.get("getBuffCubeRed", 0),
            get_buff_cube_purple=d.get("getBuffCubePurple", 0),
            get_buff_cube_green=d.get("getBuffCubeGreen", 0),
            get_buff_cube_gold=d.get("getBuffCubeGold", 0),
            get_buff_cube_sky_blue=d.get("getBuffCubeSkyBlue", 0),
            sum_get_buff_cube=d.get("sumGetBuffCube", 0),
            enter_dimension_rift=d.get("enterDimensionRift", 0),
            enter_dimension_empowered_rift=d.get("enterDimensionEmpoweredRift", 0),
            win_from_dimension_rift=d.get("winFromDimensionRift", 0),
            win_from_dimension_empowered_rift=d.get("winFromDimensionEmpoweredRift", 0),
            enter_turbulent_rift=d.get("enterTurbulentRift", 0),
            gimmick_apple_dropped=d.get("gimmickAppleDropped", 0),
            gimmick_drum_use_count=d.get("gimmickDrumUseCount", 0),
            gimmick_drum_attack_count=d.get("gimmickDrumAttackCount", 0),
            gimmick_drum_dropped_hit_count=d.get("gimmickDrumDroppedHitCount", 0),
            gimmick_evidence_locker_count=d.get("gimmickEvidenceLockerCount"),
            gimmick_evidence_locker_item=d.get("gimmickEvidenceLockerItem", []),
            gimmick_hospital_discount_rate=d.get("gimmickHospitalDiscountRate", 0),
            gimmick_grandfather_clock_use_count=d.get("gimmickGrandfatherClockUseCount", 0),
            squad_rumble_rank=d.get("squadRumbleRank"),
            total_turbine_take_over=d.get("totalTurbineTakeOver") or d.get("totalTurbineTakeover"),
            total_tk_per_min=d.get("totalTKPerMin"),
            resurrection_kit_usage_count=d.get("resurrectionKitUsageCount"),
            resurrection_kit_to_credit=d.get("resurrectionKitToCredit"),
            using_default_game_option=d.get("usingDefaultGameOption"),
            reunited_count=d.get("reunitedCount"),
            is_ml_bot=d.get("isMLBot"),
            bot_level=d.get("botLevel"),
            afk_dtm=d.get("afkDtm"),
            giveup_dtm=d.get("giveupDtm"),
            milli_tournament_kill_score=d.get("milliTournamentKillScore"),
            tournament_rank_score=d.get("tournamentRankScore"),
            tree_of_life_spawn=d.get("treeOfLifeSpawn", []),
            starting_items=d.get("StartingItems", []),
            used_normal_heal_pack=d.get("usedNormalHealPack", 0),
            used_reinforced_heal_pack=d.get("usedReinforcedHealPack", 0),
            used_normal_shield_pack=d.get("usedNormalShieldPack", d.get("usedNormalShiedPack", 0)),
            used_reinforce_shield_pack=d.get(
                "usedReinforceShieldPack", d.get("usedReinforcedShieldPack", 0)
            ),
            bought_infusion=d.get("boughtInfusion", {}),
            final_infusion=d.get("finalInfusion", []),
            scored_point=d.get("scoredPoint", []),
            kills_phase_one=d.get("killsPhaseOne"),
            kills_phase_two=d.get("killsPhaseTwo"),
            kills_phase_three=d.get("killsPhaseThree"),
            deaths_phase_one=d.get("deathsPhaseOne"),
            deaths_phase_two=d.get("deathsPhaseTwo"),
            deaths_phase_three=d.get("deathsPhaseThree"),
            infusion_re_roll_use_vf_credit=d.get("infusionReRollUseVFCredit", 0),
            infusion_trait_use_vf_credit=d.get("infusionTraitUseVFCredit", 0),
            infusion_relic_use_vf_credit=d.get("infusionRelicUseVFCredit", 0),
            infusion_store_use_vf_credit=d.get("infusionStoreUseVFCredit", 0),
            cobalt_random_pick_remove_character=d.get("cobaltRandomPickRemoveCharacter"),
            battle_zone1_area_code=d.get("battleZone1AreaCode"),
            battle_zone1_battle_mark=d.get("battleZone1BattleMark"),
            battle_zone2_area_code=d.get("battleZone2AreaCode"),
            battle_zone2_battle_mark=d.get("battleZone2BattleMark"),
            battle_zone3_area_code=d.get("battleZone3AreaCode"),
            battle_zone3_battle_mark=d.get("battleZone3BattleMark"),
            battle_zone1_winner=d.get("battleZone1Winner"),
            battle_zone2_winner=d.get("battleZone2Winner"),
            battle_zone3_winner=d.get("battleZone3Winner"),
            battle_zone1_battle_mark_count=d.get("battleZone1BattleMarkCount"),
            battle_zone2_battle_mark_count=d.get("battleZone2BattleMarkCount"),
            battle_zone3_battle_mark_count=d.get("battleZone3BattleMarkCount"),
            event_mission_result=d.get("eventMissionResult", {}),
            kill_details=d.get("killDetails", {}),
            death_details=d.get("deathDetails", {}),
            credit_source=d.get("creditSource", {}),
            food_craft_count=d.get("foodCraftCount", []),
            beverage_craft_count=d.get("beverageCraftCount", {}),
            air_supply_open_count=d.get("airSupplyOpenCount", {}),
            collect_item_for_log=d.get("collectItemForLog", []),
            equip_first_item_for_log=d.get("equipFirstItemForLog", {}),
            use_gadget=d.get("useGadget", {}),
            get_bori_reward=d.get("getBoriReward", {}),
            cc_time_to_player=d.get("ccTimeToPlayer", 0.0),
        )
